
from django import forms
from . models import Redditsubreddit



class ManyForm(forms.Form):
    bars = forms.IntegerField(label='bars', min_value=1, max_value=250 )
    days = forms.IntegerField(label='days', min_value=1, max_value=250 )
    subreddits =  forms.ModelMultipleChoiceField(queryset=Redditsubreddit.objects.all(),
                                                widget = forms.CheckboxSelectMultiple,
                                                to_field_name='subreddit')
    ticker = forms.CharField(label='Ticker', max_length=6, required=False)
  
 

class SingleForm(forms.Form):
    days = forms.IntegerField(label='bar_quantity', min_value=1, max_value=250 )
    subreddits =  forms.ModelMultipleChoiceField(queryset=Redditsubreddit.objects.all(),
                                                widget = forms.CheckboxSelectMultiple,
                                                to_field_name='subreddit')
    ticker = forms.CharField(label='Ticker', max_length=6, required=False)

