
from grapher.models import Redditpostcache, Redditsubreddit, Redditcommentcache
import ast
import datetime
from grapher import models
from ticker_manager.mixins import TickerManager
from . forms import ManyForm, SingleForm
from accounts.forms import BlackListedTickersForm


  
        
class FormSetter:
    
    def set_many_ticker_form(self, request):
        if request.method == 'POST':
            self.many_form = ManyForm(request.POST)
            if self.many_form.is_valid():
                self.days = self.many_form.cleaned_data['days']
                self.bars = self.many_form.cleaned_data['bars']
                self.subreddits = [sub.subreddit for sub in self.many_form.cleaned_data['subreddits']]
                self.ticker = self.many_form.cleaned_data['ticker']
                self.obj['ticker'] = self.ticker
                self.initial = {'bars':self.bars, 'days':self.days, 'subreddits':self.subreddits}
                return self.many_form
        else:
            self.initial = {'bars':self.bars, 'days':self.days, 'subreddits':self.subreddits}
            self.many_form = ManyForm(initial=self.initial)
            self.obj['many_form'] = self.many_form
            return self.many_form
    
    def set_user_lists_form(self, request):
        self.obj['black_list_form'] = BlackListedTickersForm()


class KwargHandler:
    def var_from_kwargs(self, request, **kwargs):
        self.obj = dict()
        try:
            self.days = kwargs['days']
        except:
            self.days = 50
        self.obj['days'] = self.days
        try:
            self.bars = kwargs['bars']
        except:
            self.bars= 30
        self.obj['bars'] = self.bars
        try:
            self.sortby = kwargs['sortby']
        except:
            self.sortby = 'sentiment'
        self.obj['sortby'] = self.sortby
        try:
            self.subreddits_list = ast.literal_eval(kwargs['subreddits'])
            self.subreddits = [ models.Redditsubreddit.objects.get(subreddit=sub) for sub in self.subreddits_list]
        except:
            self.subreddits = models.Redditsubreddit.objects.all()
            self.subreddits_list = [sub.subreddit for sub in self.subreddits]
        self.obj['subreddits'] = self.subreddits_list

        try:
            self.window = kwargs['window'] 
        except:
            self.window = 100
        try:
            self.ticker = kwargs['ticker'].upper().replace(' ', '')
            self.obj['ticker'] = self.ticker
        except:
            self.obj['ticker'] = None
        try:
            kwargs['positive_only']
            self.positive_only = True
        except:
            self.positive_only =False
        try:
            self.watch_list = kwargs['watch_list']
        except:
            self.watch_list = None
        return self.obj

class SetUserData:
    def set_user_info(self, request, **kwargs):
        try:
            self.obj
        except:
            self.obj
        self.watch_list = TickerManager(request=request).watch_list()
        self.black_list = TickerManager(request=request).black_list()
        self.obj['black_list'] = self.black_list 
        self.obj['watch_list'] = self.watch_list
        if self.request.user.is_authenticated:
            self.obj['username'] = request.user

class CustomFormater():
    def __init__(self,watch_list_tickers=[], black_list_tickers=[], num=30, days=50, subreddits=None):
        self.__output = dict()
        self._all_comments =list()
        self._all_posts = list()
        self.days = days
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=self.days)
        self._mentiond_dicts_post_comments = list()
        self._concat_all_dicts = dict()
        self.num = num
        self.black_list_tickers = [ticker.ticker for ticker in black_list_tickers]
        self.watch_list_tickers = [ticker.ticker for ticker in watch_list_tickers]
        # store raw comment qury sorted by subreddit in dict
        self.subreddit_comments = dict()
        self.subreddit_posts = dict()
        self.subreddits = subreddits
        self.total_count_dict = dict()

        self._top_ticker_all_subreddits_requested(subreddits=subreddits)

        self.colors = ['rgba(178, 171, 242)',
                'rgba(168, 130, 197)',
                'rgba(158, 88, 152)',
                'rgba(137, 4, 61)',
                'rgba(47, 230, 222)',
                'rgba(38, 139, 144)',
                'rgba(28, 48, 65)',
                'rgba(27, 97, 94)',
                'rgba(26, 145, 122)',
                'rgba(24, 242, 178)'

               ]  
    
    def _top_ticker_all_subreddits_requested(self, subreddits):
        # finds the top mentioed tickers for the subreddits requested
        # going back the amount of days requested
        self._all_comments = self._all_comments_maker()
        self._all_posts = self._all_post_maker()
        for comment in self._all_comments:
            self._mentiond_dicts_post_comments.append(ast.literal_eval(comment.comment_tickers_used))
        for post in self._all_posts:
            self._mentiond_dicts_post_comments.append(ast.literal_eval(post.title_tickers_used))
            self._mentiond_dicts_post_comments.append(ast.literal_eval(post.text_tickers_used))
        
        for ticker_dictionary in self._mentiond_dicts_post_comments:

            if self.watch_list_tickers:
                for ticker in self.watch_list_tickers:
                    try:
                        self._concat_all_dicts[ticker]
                        self._concat_all_dicts[ticker] += ticker_dictionary[ticker]
                    except KeyError:
                        try:
                            self._concat_all_dicts[ticker] = ticker_dictionary[ticker]
                        except KeyError:
                            pass

            else:
                for ticker in ticker_dictionary:
                    if ticker in self.black_list_tickers:
                        pass
                    else:
                        try:
                            self._concat_all_dicts[ticker]
                            self._concat_all_dicts[ticker] += ticker_dictionary[ticker]
                        except KeyError:
                            self._concat_all_dicts[ticker] = ticker_dictionary[ticker]
        
        self.top_tickers = list()
        for i in list(range(self.num)):
            try: # used to prevent max() called on nothig of nothing 
                ticker = max(self._concat_all_dicts, key=self._concat_all_dicts.get)
                self.top_tickers.append(ticker)
                self.total_count_dict[ticker] = self._concat_all_dicts[ticker]
                self._concat_all_dicts.pop(ticker)
            except ValueError:
                pass
    
    def _all_comments_maker(self):
        # qury all comments for the selected subreddits
        # creates self._all_comments -list of all comments qurys
        for subreddit in self.subreddits:
            self._comments = Redditcommentcache.objects.filter(subreddit=subreddit,
                    datetime__range=(
                        self.start_date.isoformat(),
                        self.end_date.isoformat()
                        ))
            self.subreddit_comments[subreddit] = self._comments
            for com in self._comments:
                self._all_comments.append(com)
        return self._all_comments

    def _all_post_maker(self):
        # qury all posts for the selected subreddits
        # creates self._all_posts -list of all posts qurys
        for subreddit in self.subreddits:
            self._posts = Redditpostcache.objects.filter(subreddit=subreddit,
                    datetime__range=(
                        self.start_date.isoformat(),
                        self.end_date.isoformat()
                        ))
            self.subreddit_posts[subreddit] = self._posts
            for post in self._posts:
                self._all_posts.append(post)
        return self._all_posts

    def create_data_subreddit(self,subreddit):
        # length=num in oder of decending populaity with interger times mentioned
        output = { ticker:0 for ticker in self.top_tickers}
        
        comments = self.subreddit_comments[subreddit]
        posts = self.subreddit_posts[subreddit]

        for ticker in self.top_tickers:
            # add all comment metions
            for com in comments:
                d = ast.literal_eval(com.comment_tickers_used)
                try:
                    d[ticker]
                    output[ticker] += d[ticker]
                except:
                    pass
            # add all posts title and text mentions
            for post in posts:
                d1 = ast.literal_eval(post.title_tickers_used)
                d1 = ast.literal_eval(post.text_tickers_used)
                try:
                    d1[ticker]
                    output[ticker] += d1[ticker]
                except:
                    pass
                try:
                    d2[ticker]
                    output[ticker] += d2[ticker]
                except:
                    pass
        return output.values()

    def build_color_list(self, color=1):
        color_list = list()
        for i in range(len(self.top_tickers)):
            color_list.append(self.colors[color])
        return color_list


class RedditSubsBar(object):
    # shows all subreddits posts and comments top 30 tickers as a stacked bar graph
    #demonstrating what subreddits contribute most to top tickers
    # template_name = 'grapher/popular_tickers_subreddit_bar.html'
    
    def get_bar_chart_obj(self,watch_list_tickers, black_list_tickers, bar_quantity, subreddits, days=10, **kwargs):
        tool = CustomFormater(watch_list_tickers=watch_list_tickers, 
                            black_list_tickers=black_list_tickers,
                            num=bar_quantity, days=days, 
                            subreddits=subreddits)
        subreddit_data = dict()
        dataset = list()
        labels = []



        for i, subreddit in enumerate(subreddits):
            data = tool.create_data_subreddit(subreddit=subreddit)
            temp_dict = {
                'label': subreddit.subreddit,
                'data': list(data),
                'backgroundColor': tool.build_color_list(color=i),
                'borderColor': tool.build_color_list(color=i),
                'borderWidth': 2
            }
            dataset.append(temp_dict)
        #create lablels with total times mentioned
        for ticker in tool.top_tickers:
            labels.append(ticker+' '+ str(tool.total_count_dict[ticker]))

        output ={
            'labels': labels,
            'datasets': dataset,
        }
        object = { 'reddit_subreddit_bar':output}
        object['showing_tickers'] = tool.top_tickers
        format = "%b %d %Y, at %I %p"
        object['from_date'] = tool.start_date.strftime(format)
        return object


class SingleTickerTool():
    
    def __init__(self, ticker, subreddits, days):
        self.ticker = ticker
        self.subreddits = subreddits
        self.days = days
        self._calc_start_end_dates()
        #used to store all commentcache for all subreddits in self.subreddits
        self._all_comments = list()
        #used to start comments sorted by subreddit
        self.subreddit_comments = dict()
        self._get_all_comments()
        # colors
        self.colors = ['rgba(178, 171, 242)',
                'rgba(168, 130, 197)',
                'rgba(158, 88, 152)',
                'rgba(137, 4, 61)',
                'rgba(47, 230, 222)',
                'rgba(38, 139, 144)',
                'rgba(28, 48, 65)',
                'rgba(27, 97, 94)',
                'rgba(26, 145, 122)',
                'rgba(24, 242, 178)'

               ]  
        self.build_color_list()
        #bar graph data initial values all 0
        self.sf = "%b %d %Y, at %I %p"
        self._initiate_bar_graph_data()
        

    def create_data(self):
        dataset=[]
        for  i, subreddit in enumerate(self.subreddit_comments):
            self._initiate_bar_graph_data()
            count = 0
            print(subreddit)
            comments = self.subreddit_comments[subreddit]
            if comments:
                for comment in comments:
                    date = str(comment.datetime.strftime(self.sf))
                    all_tickers_used = ast.literal_eval(comment.comment_tickers_used)
                    if self.ticker in all_tickers_used:
                        count = all_tickers_used[self.ticker]
                        self.bar_graph_data[date] = count



            temp_list = list(self.bar_graph_data.values())
            temp_dict = {
                'label': subreddit.subreddit,
                'data': temp_list,
                'backgroundColor': self.color_list[i],
                'borderColor': self.color_list[i],
                'borderWidth': 0
            }
            dataset.append(temp_dict)
        
        #create lablels of dates
        labels = list()
        for date in self.bar_graph_data:
            labels.append(date)

        output ={
            'labels': labels,
            'datasets': dataset
            }
        
        object = { 'reddit_subreddit_single':output}
        return object
    
    def build_color_list(self, color=1):
        self.color_list = list()
        for i in range(len(self.subreddits)):
            self.color_list.append(self.colors[i])
        return self.color_list

    def _initiate_bar_graph_data(self):
        #creates dict to track the mentions for the subreddit
        self.bar_graph_data = dict()
        i = 0
        date = self.start_date.replace(hour=0, minute=0,second=0,microsecond=0)
        while date <= self.end_date:
            date += datetime.timedelta(hours=1)
            self.bar_graph_data[date.strftime(self.sf)] = 0

    def _calc_start_end_dates(self):
        #takes days and convert too datetimes 
        self.end_date = datetime.datetime.now()
        self.start_date = self.end_date - datetime.timedelta(days=self.days)
    
    def _get_all_comments(self):
        # qury all comments for the selected subreddits
        # creates self._all_comments -list of all comments qurys
        for subreddit in self.subreddits:
            self._comments = Redditcommentcache.objects.filter(subreddit=subreddit,
                    datetime__range=(
                        self.start_date.isoformat(),
                        self.end_date.isoformat()
                        ))
            self.subreddit_comments[subreddit] = self._comments
            for com in self._comments:
                self._all_comments.append(com)
        return self._all_comments

    def get_all_posts(self):
        pass

class ColorTool:
    def __init__(self):
        self.colors = ['rgba(178, 171, 242)',
        'rgba(168, 130, 197)',
        'rgba(158, 88, 152)',
        'rgba(137, 4, 61)',
        'rgba(47, 230, 222)',
        'rgba(38, 139, 144)',
        'rgba(28, 48, 65)',
        'rgba(27, 97, 94)',
        'rgba(26, 145, 122)',
        'rgba(24, 242, 178)'
        ]  
    
    def color_sub_dict(self, subreddits):
        color_dict = dict()
        for i, sub in enumerate(subreddits):
            color_dict[sub] = self.colors[i]
        return color_dict
    
    def color_feed(self, length):
        out = list()
        count = 0
        for l in range(length):
            count += 1
            if count >= len(self.colors):
                count=0
            out.append(self.colors[count])
        return out 