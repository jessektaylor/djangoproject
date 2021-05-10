from django.shortcuts import render, redirect
from django.views.generic import  View
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect
from grapher import models
import ast
import datetime

from . tools import ColorTool, KwargHandler, SetUserData , FormSetter #CustomFormater, RedditSubsBar, SingleTickerTool, 
from django.core.exceptions import ObjectDoesNotExist
from accounts.forms import BlackListedTickersForm
from ticker_manager.mixins import TickerManager
import json
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler


class SentimentTreeView(FormSetter, SetUserData, KwargHandler, View):
    template_name =  'grapher/tree_map_sentiment.html'

    def get(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        # set date search parameters
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days)
        #### get user blacklist, watchlist if requested
        # returns my black list if not not a user
        try:
            #no include
            kwargs['watch_list']
            
            tickers_qury = models.Cachetoptickerssentiment.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list,
                    ticker__in=self.watch_list).values('ticker','count','datetime','sentiment','subreddit')
        except KeyError:
            black_list = [bl.ticker for bl in self.black_list ]
            tickers_qury = models.Cachetoptickerssentiment.objects.filter(
                        datetime__range=(start_date, end_date), 
                        subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime','sentiment','subreddit')

        columns=['ticker','count','datetime','sentiment','subreddit']
        df = pd.DataFrame(tickers_qury, columns=columns)
        sentiment = pd.pivot_table(df, index=['ticker'], values=['sentiment'], aggfunc=np.mean)
        counts = pd.pivot_table(df, index=['ticker'], values=['count'], aggfunc=np.sum)
        final_df = sentiment.merge(counts['count'],left_index=True, right_index=True )
        final_df = final_df.sort_values('count', ascending=False)

        if self.positive_only:
            final_df = final_df[final_df.sentiment > 0]
        # chop off rows that are not needed
        final_df = final_df.head(self.bars)
        
        #create price data
        self.yahoo_price_data(start_date, end_date, list(final_df.index))

        # create datasets list and colorlist
        datasets = [['Location','Parent','Count','Sentiment', 'link'],['Global','',0,0,0]]

        for index, row in final_df.iterrows():
            link = '{{% url "grapher:SingleSentiment" ticker="{}" %}}'.format(index)
            # link = 'https//google.com'
            datasets.append(
                [index, 'Global' , row['count'], row['sentiment'], link]
            )
  
        self.obj['datasets'] = str(datasets)
        self.obj['tickers'] = list(final_df.index)
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        return render(request, self.template_name, self.obj)

    def post(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        if self.obj['ticker']:
            return HttpResponseRedirect(reverse('grapher:SingleSentiment',  kwargs={'ticker': self.obj['ticker']} ))
     
        return HttpResponseRedirect(reverse('grapher:SentimentTreeView',  kwargs=kwargs_values ))


    def yahoo_price_data(self, start_date, end_date, tickers):
        print(start_date, end_date)
        # for ticker in tickers:
        yahoo_qury = models.Historicalyahoo.objects.filter(
                        datetime__range=(start_date, end_date), 
                        ticker__in=tickers).values('ticker','datetime','open','high','low', 'close', 'adjclose', 'volume')
        if yahoo_qury:
            columns=['ticker','datetime','open','high','low', 'close', 'adjclose', 'volume']
            df = pd.DataFrame(yahoo_qury, columns=columns)
            # find interables
            unique_tickers = df['ticker'].unique()
            unique_dates = df['datetime'].unique()
            # index by ticker and datetime
            df = df.groupby([ 'ticker', 'datetime']).mean()
            # create var to give to tempate
            out =list()
            
            for tic in unique_tickers:
                # make new df with only single ticker value
                _df = df.loc[tic]
                _df.dropna(inplace=True)
                _df = _df[::-1]
                # statard diviation
                _df['pct_change'] = _df['adjclose'].pct_change(2)
                stadard_divation = _df['pct_change'].std()
                # actual percent change for time period
                percent_change = ((_df['adjclose'][0] - _df['adjclose'][-1]) /  _df['adjclose'][-1]) *100
                # volume first half compared to second half
                volume_second_half =  _df['volume'][_df.shape[0]//2:].sum() - _df['volume'][:_df.shape[0]//2].sum()
                # increase from total volume mean 
                vol = volume_second_half / _df['volume'].mean()
                # save stats to inner dictionary
    
                inner = {
                    'ticker':tic,
                    'std':stadard_divation,
                    'pct_change':percent_change,
                    'date':_df.index[0],
                    'adjclose': _df['adjclose'][0],
                    'volume_stat':vol,
                    'pct_color':self.color_it(percent_change),
                    'vol_color':self.color_it(vol),
                }
                out.append(inner)
            d = pd.DataFrame(out)
            
            d = d.sort_values('ticker',  ascending=True)
            self.obj['stock_data'] = d.T.to_dict().values()

            # Backtest data
            inital_value = 10000
            cap_per = inital_value / d.shape[0]
            d['change'] = (d['pct_change']/100) * cap_per
           
            self.obj['portfolio_start'] = inital_value
            self.obj['portfolio_end'] = d['change'].sum() + inital_value
            self.obj['portfolio_end_color'] = self.color_it(self.obj['portfolio_end'])
            self.obj['percent_mean'] = d['pct_change'].mean()
            self.obj['percent_mean_color'] = self.color_it(self.obj['percent_mean'])
            self.obj['percent_mean_color'] = self.color_it(d['pct_change'].mean())
            self.obj['std_mean'] = d['std'].mean()
            self.obj['volume_mean'] = d['volume_stat'].mean()
            self.obj['volume_mean_color'] = self.color_it(self.obj['volume_mean'] )
            days =  end_date -start_date 
            self.obj['anual_return'] = (1 / (days.days/365)) * d['pct_change'].mean()
            self.obj['anual_return_color'] = self.color_it(self.obj['anual_return'])
        
    
    def color_it(self, value):
        if value:
            if value > 0:
                return 'green'
            if value < 0:
                return 'red'
      
            
class BubbleSentimentView(SentimentTreeView, FormSetter,SetUserData, KwargHandler, View):
    template_name =  'grapher/bubble_sentiment.html'
   
    def get(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        # set date search parameters
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days)
        #### get user blacklist, watchlist if requested
        # returns my black list if not not a user
        try:
            #no include
            kwargs['watch_list']
            watch_list_qury = TickerManager(request=request).watch_list()
            self.black_list
            tickers_qury = models.Cachetoptickerssentiment.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list).include(ticker__in=black_list).values('ticker','count','datetime','sentiment','subreddit')
        except KeyError:
            black_list_qury = TickerManager(request=request).black_list()
            black_list = [bl.ticker for bl in black_list_qury ]
            tickers_qury = models.Cachetoptickerssentiment.objects.filter(
                        datetime__range=(start_date, end_date), 
                        subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime','sentiment','subreddit')

        columns=['ticker','count','datetime','sentiment','subreddit']
        df = pd.DataFrame(tickers_qury, columns=columns)
        sentiment = pd.pivot_table(df, index=['ticker'], values=['sentiment'], aggfunc=np.mean)
        counts = pd.pivot_table(df, index=['ticker'], values=['count'], aggfunc=np.sum)
        final_df = sentiment.merge(counts['count'],left_index=True, right_index=True )
        final_df = final_df.sort_values('count', ascending=False)

        if self.positive_only:
            final_df = final_df[final_df.sentiment > 0]
        final_df = final_df[:self.bars]
       
        # pixel range for bubbles 4, 40
        scaler = MinMaxScaler(feature_range=(4,40))
        # min max scales the column between feature_range
        final_df['diameter'] = scaler.fit_transform(final_df['count'].values.reshape(-1,1))
        
        # create datasets list and colorlist
        datasets = list()
        color_list = ColorTool().color_feed(final_df.shape[0])
        i=0 # counter used for color list
        for index, row in final_df.iterrows():
            datasets.append(
                {
                    'label':[ str(index)],
                    'backgroundColor': color_list[i],
                    'borderColor': color_list[i],
                    'data': [{
                        'x': row['sentiment'],
                        'y': row['count'],
                        'r': row['diameter']
                    }]
                }
            )
            i+=1

        self.obj['datasets'] = datasets
        self.yahoo_price_data(start_date, end_date, list(final_df.index))
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
            'sortby': self.sortby
        }
        
        return render(request, self.template_name, self.obj)
    
    def post(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
      
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
            'sortby':self.sortby,
        }
        if self.obj['ticker']:
            
            return HttpResponseRedirect(reverse('grapher:SingleSentiment',  kwargs={'ticker': self.obj['ticker']} ))
        
        return HttpResponseRedirect(reverse('grapher:BubbleSentimentView',  kwargs=kwargs_values ))


class LiteralView(SentimentTreeView, FormSetter, SetUserData, KwargHandler, View):
    template_name =  'grapher/literal_bar_full.html'
    
    def get(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        # set date search parameters
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days)
        # set black list
        black_list_qury = TickerManager(request=request).black_list()
        black_list = [bl.ticker for bl in black_list_qury ]
        # qury the nouns
        tickers_qury = models.Cachetoptickersliteral.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime', 'subreddit')
        tickers_qury_post = models.Cachetoptickersliteralposts.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime','subreddit')  
        # do data calc on qury
        columns=['ticker','count','datetime','subreddit']
        df = pd.DataFrame(tickers_qury, columns=columns)
        df = pd.pivot_table(df, index=['ticker'], values=['count'], aggfunc=np.sum)
        columns=['ticker','count','datetime','subreddit']
        df2 = pd.DataFrame(tickers_qury_post, columns=columns)
        df2 = pd.pivot_table(df2, index=['ticker'], values=['count'], aggfunc=np.sum)
        # merge two datasets and sum the rows
        final_df = df.merge(df2['count'],left_index=True, right_index=True )
        final_df = final_df.sum(axis=1)
        
        final_df = final_df.sort_values(0, ascending=False)
        final_df = final_df.head(self.bars)
        
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        self.obj['data'] = list(final_df.values)
        self.obj['labels'] = [ str(date) for date in final_df.index]
        self.obj['colors'] = ColorTool().color_feed(length=final_df.shape[0])
        self.yahoo_price_data(start_date, end_date, list(final_df.index))
        return render(request, self.template_name, self.obj)
    
    def post(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
      
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        if self.obj['ticker']:
            return HttpResponseRedirect(reverse('grapher:SingleSentiment',  kwargs={'ticker': self.obj['ticker']} ))
        return HttpResponseRedirect(reverse('grapher:LiteralView',  kwargs=kwargs_values ))


class NounView(SentimentTreeView, FormSetter, SetUserData,KwargHandler, View):
    template_name =  'grapher/noun_bar_full.html'
    def get(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        # set date search parameters
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days)
        # set black list
        black_list_qury = TickerManager(request=request).black_list()
        black_list = [bl.ticker for bl in black_list_qury ]
        # qury the nouns
        tickers_qury = models.Cachetoptickersnoun.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime', 'subreddit')
        tickers_qury_post = models.Cachetoptickersnounpost.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime','subreddit')  
        # do data calc on qury
        columns=['ticker','count','datetime','subreddit']
        df = pd.DataFrame(tickers_qury, columns=columns)
        df = pd.pivot_table(df, index=['ticker'], values=['count'], aggfunc=np.sum)
        columns=['ticker','count','datetime','subreddit']
        df2 = pd.DataFrame(tickers_qury_post, columns=columns)
        df2 = pd.pivot_table(df2, index=['ticker'], values=['count'], aggfunc=np.sum)
        # merge two datasets and sum the rows
        final_df = df.merge(df2['count'],left_index=True, right_index=True )
        final_df = final_df.sum(axis=1)
        
        final_df = final_df.sort_values(0, ascending=False)
        final_df = final_df.head(self.bars)
      

        self.obj['data'] = list(final_df.values)
        self.obj['labels'] = [ str(date) for date in final_df.index]
        self.obj['colors'] = ColorTool().color_feed(length=final_df.shape[0])
        self.yahoo_price_data(start_date, end_date, list(final_df.index))
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        
        return render(request, self.template_name, self.obj)

    def post(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
      
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        if self.obj['ticker']:
            return HttpResponseRedirect(reverse('grapher:SingleSentiment',  kwargs={'ticker': self.obj['ticker']} ))
        return HttpResponseRedirect(reverse('grapher:NounView',  kwargs=kwargs_values )) 


class SingleSenitmentView(KwargHandler, View):
    template_name =  'grapher/single_sentiment_full.html'

    def get(self, request, *args, **kwargs):
        obj = dict()
        self.obj = self.var_from_kwargs(request, **kwargs)
        # create start and end dates
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days)
        qury = models.Cachetoptickerssentiment.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list,
                    ticker=self.ticker).values('ticker','count','datetime','sentiment','subreddit')
        columns=['ticker','count','datetime','sentiment','subreddit']
        df = pd.DataFrame(qury, columns=columns)
        df = pd.pivot_table(df, index=['datetime'], values=['sentiment', 'count'], aggfunc={'sentiment':np.mean, 'count':np.sum})
        df['rolling_sentiment'] = df['sentiment'].rolling(self.window).mean()
        df['rolling_count'] = df['count'].rolling(self.window).sum()
        df = df[self.window:]
  
        self.obj['max_value']= df['rolling_sentiment'].max()
        self.obj['min_value'] = df['rolling_sentiment'].min()
        # get price data
        
        yahoo_qury = models.Historicalyahoo.objects.filter(
                        datetime__range=(start_date, end_date), 
                        ticker=self.ticker).values('datetime','open','high','low', 'close', 'adjclose', 'volume')
        df_price = pd.DataFrame(yahoo_qury)
        df_price.set_index('datetime', inplace=True)
        df = df.join(df_price)
        df.interpolate(method='linear',axis=0, inplace=True, limit_direction='both')
     

        data = [['date','sentiment','Price']]
        for index, row in df.iterrows():
            
            mini_list = [str(index.strftime('%m-%d-%Y')) ,  row['rolling_sentiment'] ,row['adjclose']]
            data.append(mini_list)
      
        self.obj['data'] = data
        self.obj['ticker'] = self.ticker
        self.obj['percent_change'] = ((df['adjclose'][-1] - df['adjclose'][0]) / df['adjclose'][0]) *100
        self.obj['percent_change_color'] = self.color_it(self.obj['percent_change'])
        self.obj['max_price'] = df_price['high'].max()
        self.obj['min_price'] = df_price['low'].min()

        return render(request, self.template_name, self.obj)
    
    
    def color_it(self, value):
        if value:
            if value > 0:
                return 'green'
            if value < 0:
                return 'red'


class SentimentView(SentimentTreeView, FormSetter, SetUserData,KwargHandler, ColorTool, View):
    # get method always called
    template_name =  'grapher/sentiment_full.html'
   
    
    def get(self, request, *args, **kwargs):
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        # set date search parameters
        end_date = datetime.datetime.now()
        start_date = end_date - datetime.timedelta(days=self.days)
        #### get user blacklist, watchlist if requested
        # returns my black list if not not a user
        if self.watch_list:
            watch_list_qury = TickerManager(request=request).watch_list()
            tickers_qury = models.Cachetoptickerssentiment.objects.filter(
                    datetime__range=(start_date, end_date), 
                    subreddit__in=self.subreddits_list,
                    ticker__in=self.watch_list).values('ticker','count','datetime','sentiment','subreddit')
        else:
            black_list_qury = TickerManager(request=request).black_list()
            black_list = [bl.ticker for bl in black_list_qury ]
            tickers_qury = models.Cachetoptickerssentiment.objects.filter(
                        datetime__range=(start_date, end_date), 
                        subreddit__in=self.subreddits_list).exclude(ticker__in=black_list).values('ticker','count','datetime','sentiment','subreddit')

        columns=['ticker','count','datetime','sentiment','subreddit']
        df = pd.DataFrame(tickers_qury, columns=columns)
        sentiment = pd.pivot_table(df, index=['ticker'], values=['sentiment'], aggfunc=np.mean)
        counts = pd.pivot_table(df, index=['ticker'], values=['count'], aggfunc=np.sum)
        final_df = sentiment.merge(counts['count'],left_index=True, right_index=True )
        final_df = final_df.sort_values(self.sortby, ascending=False)
        final_df = final_df.head(self.bars)
        
        self.obj['labels'] = list(final_df.index)
        if self.sortby =='count':
            self.obj['dataset_labels'] = list(final_df['count'])
        elif self.sortby == 'sentiment':
            self.obj['dataset_labels'] = list(final_df['sentiment'])
        
        self.obj['data'] = list(final_df['sentiment'])
        self.obj['backgroundColor'] = self.color_feed(self.bars)
        initial = {'bars':self.bars, 'days':self.days, 'subreddits':self.subreddits}

        self.yahoo_price_data(start_date, end_date, list(final_df.index))
        
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
        }
        return render(request, self.template_name, self.obj)


    #post will route all request to get with updated kwargs
    def post(self, request, *args, **kwargs):
        obj =dict()
        self.obj = self.var_from_kwargs(request, **kwargs)
        self.set_user_info(request)
        self.set_many_ticker_form(request)
        self.set_user_lists_form(request)
        # if form.is_valid():
        #     days = form.cleaned_data['days']
        #     bars = form.cleaned_data['bars']
        #     print(form.cleaned_data['subreddits'])
        #     subreddits = [sub.subreddit for sub in form.cleaned_data['subreddits']]
        #     ticker = form.cleaned_data['ticker']
        
        try:
            sortby = kwargs['sortby']
        except:
            sortby = 'sentiment'
        kwargs_values = {
            'days':self.days, 
            'bars':self.bars,
            'subreddits':str(self.subreddits),
            'sortby':self.sortby,
        }
        obj['BlackListedTickersForm'] = BlackListedTickersForm
        if self.obj['ticker']:
            return HttpResponseRedirect(reverse('grapher:SingleSentiment',  kwargs={'ticker': self.obj['ticker']} ))
        return HttpResponseRedirect(reverse('grapher:SentimentView',  kwargs=kwargs_values ))





# class SubredditLiteralBarView( RedditSubsBar, View):
#     template_name =  'grapher/subRedditLiteralBar.html'
    
#     form_class = RedditBarForm
#     form_black_list = BlackListedTickersForm
#     initial= {'bar_quantity':20,
#             'days':14,
#             'subreddits':Redditsubreddit.objects.all(),
#             }

#     def get(self, request, *args, **kwargs):
#         # if ticker specified then route to the single ticker view
#         try:
#             kwargs_values={'ticker':kwargs['ticker'],
#                 'days':kwargs['days'],
#                 'subreddit_ids':kwargs['subreddit_ids']}
#             return HttpResponseRedirect(reverse('grapher:singleticker', kwargs=kwargs_values))
#         except KeyError:
#             pass
#         # Set watch list if requested
#         try: # set watch list
#             exists = kwargs['view_watch_list']
#             if exists == 'view_watch_list': # explicit to use watch list
#                 watch_list_tickers = TickerManager(request=request).watch_list()
#             elif exists == 'dontViewWatchList': # explicit don't use watch list
#                 watch_list_tickers = []
#         except KeyError: # watchlist varible was not found set to empty list
#             watch_list_tickers = []
        
#         # if kwargs are given from post set the varibles
#         try:
#             initial = {
#                 'bar_quantity' : kwargs['bar_quantity'],
#                 'days' : kwargs['days'],
#                 'subreddits' : [Redditsubreddit.objects.get(id=id) for id in ast.literal_eval(kwargs['subreddit_ids'])],
#                 'view_watch_list' : kwargs['view_watch_list']
#                 }
#         except KeyError:
#             initial = self.initial


#         # create data from tool 
#         obj = self.get_bar_chart_obj(
#                             watch_list_tickers=watch_list_tickers,
#                             black_list_tickers=TickerManager(request=request).black_list(),
#                             bar_quantity=initial['bar_quantity'],
#                             subreddits = initial['subreddits'],
#                             days=initial['days'])

#         # add forms to context

#         obj['BlackListedTickersForm'] = BlackListedTickersForm
#         obj['form'] = RedditBarForm(initial=initial)
        
#         # add showing tickers as qurys to context
#         ticker_qurys = self._ticker_list_to_quyset(obj['showing_tickers'])
#         obj['ticker_qurys'] = ticker_qurys

#         # add user black list and watch list
#         obj['user_black_list'] = TickerManager(request=request).black_list() 
#         obj['user_watch_list'] = TickerManager(request=request).watch_list()  
#         return render(request, self.template_name, obj)

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             days = form.cleaned_data['days']
#             bar_quantity = form.cleaned_data['bar_quantity']
#             subreddits = [sub.id for sub in form.cleaned_data['subreddits']]
#             ticker = form.cleaned_data['ticker']
#             view_watch_list = 'dontViewWatchList'
#         kwargs_values = {
#             'days':days,
#             'bar_quantity':bar_quantity,
#             'subreddit_ids':str(subreddits),
#             'view_watch_list':view_watch_list
#         }
#         if ticker:
#             kwargs_values['ticker'] = ticker

#         return HttpResponseRedirect(reverse('grapher:SubredditLiteralBarPost', kwargs=kwargs_values))


#     def _ticker_list_to_quyset(self, ticker_list):
#         ticks = list()
#         for ticker in ticker_list:
#             try:
#                 nyse_ticks = Nysetickers.objects.get(ticker=ticker)
#                 if nyse_ticks:
#                     ticks.append(nyse_ticks)
#             except:
#                 pass
#             try:
#                 nasdaq_ticks = Nasdaqtickers.objects.get(ticker=ticker)
#                 if nasdaq_ticks:
#                     ticks.append(nasdaq_ticks)
#             except:
#                 pass
#         return ticks


# class SingleLiteralTickerView(View):
#     # get method always called
#     template_name =  'grapher/single_ticker.html'
#     RedditSingleForm = RedditSingleForm
    

#     # post will route all request to get with updated kwargs
#     def post(self, request, *args, **kwargs):
#         single_form = RedditSingleForm(request.POST)
#         if single_form.is_valid():
#             ticker = single_form.cleaned_data['ticker']
#             days = single_form.cleaned_data['days']
#             subreddits = single_form.cleaned_data['subreddits']
#             subreddit_ids = [sub.id for sub in subreddits]
#             kwargs_values={'ticker':ticker,
#                     'days':days,
#                     'subreddit_ids':str(subreddit_ids)}
#             return HttpResponseRedirect(reverse('grapher:singleticker', kwargs=kwargs_values))
    
#     def get(self, request, *args, **kwargs):
#         # get need all kwargs to work
#         ticker = kwargs['ticker'].upper()
#         print(ticker)
#         found = self._is_ticker_found( kwargs)
#         if not found:
#             return HttpResponseRedirect(reverse('ticker_manager:tickernotfound', kwargs={'ticker':kwargs['ticker'].upper()}))
#         print('passed')
#         days= kwargs['days']
#         # turn string subreddits ids to qurys
#         subreddit_ids_str = kwargs['subreddit_ids']
#         subreddit_ids_list = ast.literal_eval(subreddit_ids_str)
#         subreddit_qurys = [Redditsubreddit.objects.get(id=sub) for sub in subreddit_ids_list]
#         # use tool to create graph data 
#         tool = SingleTickerTool(ticker=ticker,
#                         subreddits=subreddit_qurys,
#                         days=days)
#         obj = tool.create_data()

#         # load intital data for the single ticker form
#         initial = {
#             'days':kwargs['days'],
#             'ticker':kwargs['ticker'],
#             'subreddits':subreddit_qurys
#             }
#         try: # reset form to default if requested
#             if kwargs['initial_reset'] == 'resetForm':
#                 initial = {
#                 'days':30,
#                 'ticker':kwargs['ticker'],
#                 'subreddits':Redditsubreddit.objects.all()
#                 }
#         except:
#             pass
#         # add aditional context for template
#         obj['ticker'] = ticker
#         obj['form'] =self.RedditSingleForm(initial=initial)
#         obj['days'] = kwargs['days'] # used in {% url %}
#         obj['subreddit_ids'] = kwargs['subreddit_ids'] #used in {% url %}
#         return render(request, self.template_name, obj)

#     def _is_ticker_found(self, kwargs):
#         # try to qury ticker from DB if not there then redirct to tickernotfound manager
#         found = False
#         try:
#             qury = Nysetickers.objects.get(ticker=kwargs['ticker'].upper())
#             found = True
#         except ObjectDoesNotExist:
#             pass
#         try:
#             qury = Nasdaqtickers.objects.get(ticker=kwargs['ticker'].upper())
#             found = True
#         except ObjectDoesNotExist:
#             pass
#         return found
        



