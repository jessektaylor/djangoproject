from django.urls import path

from . import views

app_name = 'ticker_manager'

urlpatterns = [
    path('<str:ticker>/notfound/', views.TickerNotFoundView.as_view(), name='tickernotfound'),
    path('<str:ticker>/request-ticker/', views.TickerNotFoundSucessView.as_view(), name='tickernotfoundsucess')
]