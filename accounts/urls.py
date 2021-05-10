from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView


app_name = 'accounts'


urlpatterns = [
    
    path("add_ticker_to_black_list/", views.AddTickerToBlackList.as_view(), name="add_ticker_to_black_list"),
    path("add_ticker_to_black_list/<str:ticker>", views.AddTickerToBlackList.as_view(), name="add_ticker_to_black_list"),
    path("remove_ticker_from_black_list/<str:ticker>", views.RemoveTickerFromBlackList.as_view(), name="remove_ticker_from_black_list"),

    path("add_ticker_to_watch_list/", views.AddTickerToWatchList.as_view(), name="add_ticker_to_watch_list"),
    path("remove_ticker_from_watch_list/<str:ticker>", views.RemoveTickerFromWatchList.as_view(), name="remove_ticker_from_watch_list"),
    
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name='registration/login.html'), name="login"),
    path("login_required/", LoginView.as_view(template_name='registration/login_required.html'), name="login_required"),
    path("login_required/<str:ticker>", LoginView.as_view(template_name='registration/login_required.html'), name="login_required"),
    
]