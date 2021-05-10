from django.core.exceptions import ObjectDoesNotExist
from accounts.models import BlackListedTickers, WatchListTickers
from django.contrib.auth.models import User


class TickerManager:
    def __init__(self, request):
        self.request = request
 
        self.black_list()
    
    def black_list(self):
        if self.request.user.is_authenticated:
            try: # try to fetch black listed tickers
                self.black_list_tickers = BlackListedTickers.objects.filter(user=self.request.user)
            except ObjectDoesNotExist:
                # set to my blacklist
                self.black_list_tickers = BlackListedTickers.objects.filter(user=self.request.user)
        else:
            user = User.objects.get(id=2)
            self.black_list_tickers = BlackListedTickers.objects.filter(user=user)
        return self.black_list_tickers
    
    def watch_list(self):
        if self.request.user.is_authenticated:
            try: # try to fetch black listed tickers
                self.watch_list_tickers = WatchListTickers.objects.filter(user=self.request.user)
            except ObjectDoesNotExist:
                # set to my blacklist
                self.watch_list_tickers = WatchListTickers.objects.filter(user=self.request.user)
        else:
            user = User.objects.get(id=2)
            self.watch_list_tickers = WatchListTickers.objects.filter(user=user)
        return self.watch_list_tickers