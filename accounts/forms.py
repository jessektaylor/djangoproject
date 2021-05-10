


from django import forms

class BlackListedTickersForm(forms.Form):
    ticker = forms.CharField(label='Ticker', max_length=10, required=True)
