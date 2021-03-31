from django.views.generic import View
from django.shortcuts import redirect
from grapher.views import RedditSubsBar, SingleTickerTool
from grapher.models import Redditsubreddit
import psycopg2
import os
from grapher.forms import RedditBarForm, RedditSingleForm
from django.shortcuts import render
import re




class HomeView(RedditSubsBar, View):
    template_name =  'home.html'

    form_class = RedditBarForm
    initial= {'bar_quantity':20,
            'days':14,
            'subreddits':Redditsubreddit.objects.all(),
            }
    
    def get(self, request, *args, **kwargs):

        obj = self.get_bar_chart_obj(bar_quantity=self.initial['bar_quantity'],
                                 subreddits = self.initial['subreddits'],
                                  days=self.initial['days'])
        obj['form'] = self.form_class(initial=self.initial)
        ticks = list()
        for ticker in obj['showing_tickers']:
            ticks.append(Stockticker2.objects.get(ticker=ticker))
        obj['ticker_qurys'] = ticks

        # obj['watch_list'] = UserWatchList.objects.get()
        return render(request, self.template_name, obj)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # if selected to search ticker redirect to single ticker view
            if form.cleaned_data['ticker']:
                return redirect('/'+form.cleaned_data['ticker'])
            # no ticker requested show all and update parameters
            subreddit = form.cleaned_data['subreddits']
            bar_quantity = form.cleaned_data['bar_quantity']
            days = form.cleaned_data['days']
            obj = self.get_bar_chart_obj(bar_quantity=bar_quantity, subreddits=subreddit, days=days)
            obj['form'] = form
            ticks = list()
            for ticker in obj['showing_tickers']:
                ticks.append(Stockticker2.objects.get(ticker=ticker))
            
            obj['ticker_qurys'] = ticks
            return render(request, self.template_name, obj)
        return render(request, self.template_name, {'form': form})


class SingleTickerView(View):
    template_name =  'single_ticker.html'
    form_class = RedditSingleForm
    subs = Redditsubreddit.objects.all()
    days = 30
    initial= {'days':days,
            'subreddits':subs,
            }
  
    def get(self, request, *args, **kwargs):
        ticker = kwargs['ticker'].upper()
        # redirect if the ticker does not exists in db
        try:
            qury = Stockticker2.objects.get(ticker=ticker)
        except:
            return redirect('/'+ ticker+'/notfound/')

        try: # try load form data or fill with inital values
            sub_list = list()
            for id in request.session['temp_subs_ids']:
                sub_list.append(Redditsubreddit.objects.get(id=id))
            self.subs = sub_list
            self.days = request.session['temp_days']
            f = self.form_class(
                initial = {
                    'days':self.days,
                    'ticker':qury.ticker,
                    'subreddits':self.subs
                    }
                    )
        except Exception as e:
            f = self.form_class(initial=self.initial)
            print(e)
        try:
            kwargs['initial_reset']
            f = self.form_class(initial=self.initial)
        except KeyError:
            pass
        except Exception as e:
            print(e)

        tool = SingleTickerTool(ticker= qury.ticker,
                        subreddits=self.subs,
                        days=self.days)
        obj = tool.create_data()
        obj['form'] = f
        obj['ticker'] = ticker
        return render(request, self.template_name, obj)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            print('valid')
            days = form.cleaned_data['days']
            subs = form.cleaned_data['subreddits']
            ticker = form.cleaned_data['ticker'].upper()
            # if not ticker submitted on form set the the url ticker
            if not ticker:
                ticker = kwargs['ticker'].upper()
            subs_ids = [sub.id for sub in subs]
            request.session['temp_days'] = days
            request.session['temp_subs_ids'] = subs_ids
            return redirect('/'+ ticker)


class TickerNotFoundView(View):
    def get(self, request, *args, **kwargs):
        obj = {}
        obj['ticker'] = self.formate_ticker(kwargs['ticker'])

        return render(request, 'ticker_does_not_exists.html', obj)

    def formate_ticker(self, ticker):
        ticker.replace(' ', '')
        ticker.upper()
        ticker = re.sub(r'[^A-Za-z0-9 ]+', '',ticker)
        return ticker


class TickerNotFoundSucessView(View):
    def get(self, request, *args, **kwargs):
        obj = {}
        obj['ticker'] = kwargs['ticker']
        got = RequestedTicker.objects.get_or_create(ticker=kwargs['ticker'])
        print(got)
        if got:
            print('already exists')
            return render(request, 'ticker_does_not_exists_fail.html', obj)
        else:
            print('createing')
            return render(request, 'ticker_does_not_exists_sucess.html', obj)
