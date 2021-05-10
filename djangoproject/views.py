from django.views.generic import View
from django.shortcuts import redirect
# from grapher.views import RedditSubsBar, SingleTickerTool
from grapher.models import Redditsubreddit, Nasdaqtickers, Nysetickers
from django.views.generic import TemplateView
import psycopg2
import os
# from grapher.forms import RedditBarForm, RedditSingleForm
from django.shortcuts import render
import re





def HomeView(request):
    return redirect('grapher/SentimentTreeView')


