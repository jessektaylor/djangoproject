from django.views.generic import View
from django.shortcuts import redirect
import psycopg2
import os
# from grapher.forms import RedditBarForm, RedditSingleForm
from django.shortcuts import render
import re

class TickerNotFoundView(View):
    def get(self, request, *args, **kwargs):
        obj = {}
        obj['ticker'] = self.formate_ticker(kwargs['ticker'])

        return render(request, 'ticker_manager/ticker_does_not_exists.html', obj)

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
