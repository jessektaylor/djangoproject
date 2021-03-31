
from django import forms
from . models import Redditsubreddit



class RedditBarForm(forms.Form):
    bar_quantity = forms.IntegerField(label='bar_quantity', min_value=1, max_value=250 )
    days = forms.IntegerField(label='bar_quantity', min_value=1, max_value=250 )
    subreddits =  forms.ModelMultipleChoiceField(queryset=Redditsubreddit.objects.all(),
                                                widget = forms.CheckboxSelectMultiple,
                                                to_field_name='subreddit')
    ticker = forms.CharField(label='Ticker', max_length=6, required=False)
    # watchlist = forms.ModelMultipleChoiceField(to_field_name='watchlist')
    # blacklist = forms.ModelMultipleChoiceField(to_field_name='blacklist')

class RedditSingleForm(forms.Form):
    days = forms.IntegerField(label='bar_quantity', min_value=1, max_value=250 )
    subreddits =  forms.ModelMultipleChoiceField(queryset=Redditsubreddit.objects.all(),
                                                widget = forms.CheckboxSelectMultiple,
                                                to_field_name='subreddit')
    ticker = forms.CharField(label='Ticker', max_length=6, required=False)
