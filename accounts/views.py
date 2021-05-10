from django.urls import reverse_lazy, reverse
from django.views import generic
from . import forms
from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import  View, FormView
from . models import BlackListedTickers, WatchListTickers
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from ticker_manager.models import Nasdaqtickers, Nysetickers
from django.contrib.auth.models import User
from django.urls import resolve
from django.http import HttpResponseRedirect

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class AddTickerToBlackList(LoginRequiredMixin, View):
    balck_list_form = forms.BlackListedTickersForm\

    def get(self, request, *args, **kwargs):
        obj = dict()
        self.ticker = kwargs['ticker']
        self._formate_ticker()
        obj['ticker'] = self.ticker # add to context for template
        obj['blacklist'] = BlackListedTickers.objects.filter(user=request.user)
        found = self._check_if_ticker_in_db()
        if found:# if ticker in db then add to black list
            qury = BlackListedTickers.objects.get_or_create(ticker=self.ticker,user=request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    def post(self, request, *args, **kwargs):
        print('post')
        balck_list_form = self.balck_list_form(request.POST)
        obj = dict()
        obj['form'] = balck_list_form
        if balck_list_form.is_valid():
            print('valid')
            self.ticker = balck_list_form.cleaned_data['ticker']
            self._formate_ticker() # make capital remove spaces
            obj['ticker'] = self.ticker # add to context for template
            obj['blacklist'] = BlackListedTickers.objects.filter(user=request.user)
            found = self._check_if_ticker_in_db()
            if found:# if ticker in db then add to black list
                qury = BlackListedTickers.objects.get_or_create(ticker=self.ticker,user=request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def _formate_ticker(self):
        self.ticker = self.ticker.upper().replace(' ','')

    def _check_if_ticker_in_db(self):
        found =False
        try:
            nyse_ticker = Nysetickers.objects.get(ticker=self.ticker)
            if nyse_ticker:
                found =True
        except ObjectDoesNotExist:
                pass
        try:
            nasdaq_ticker = Nasdaqtickers.objects.get(ticker=self.ticker)
            if nasdaq_ticker:
                found =True
        except ObjectDoesNotExist:
            pass
        return found


class RemoveTickerFromBlackList(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        ticker = kwargs['ticker']
        qury = BlackListedTickers.objects.get(user=request.user, ticker=ticker)
        qury.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class AddTickerToWatchList(LoginRequiredMixin, View):
    balck_list_form = forms.BlackListedTickersForm
    
    def post(self, request, *args, **kwargs):
        balck_list_form = self.balck_list_form(request.POST)
        obj = dict()
        obj['form'] = balck_list_form
        if balck_list_form.is_valid():
            self.ticker = balck_list_form.cleaned_data['ticker']
            self._formate_ticker() # make capital remove spaces
            obj['ticker'] = self.ticker # add to context for template
            obj['blacklist'] = WatchListTickers.objects.filter(user=request.user)
            found = self._check_if_ticker_in_db()
            if found:# if ticker in db then add to black list
                qury = WatchListTickers.objects.get_or_create(ticker=self.ticker,user=request.user)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def _formate_ticker(self):
        self.ticker = self.ticker.upper().replace(' ','')

    def _check_if_ticker_in_db(self):
        found =False
        try:
            nyse_ticker = Nysetickers.objects.get(ticker=self.ticker)
            if nyse_ticker:
                found =True
        except ObjectDoesNotExist:
                pass
        try:
            nasdaq_ticker = Nasdaqtickers.objects.get(ticker=self.ticker)
            if nasdaq_ticker:
                found =True
        except ObjectDoesNotExist:
            pass
        return found


class RemoveTickerFromWatchList(LoginRequiredMixin, View):

    def get(self, request, **kwargs):
        ticker = kwargs['ticker']
        try:
            qury = WatchListTickers.objects.get(user=request.user, ticker=ticker)
            qury.delete()
        except:
            pass
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
