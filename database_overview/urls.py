from django.urls import path

from .views import DataBaseOverView

app_name = 'database_overview'
urlpatterns = [
    path('all/', DataBaseOverView.as_view(), name='DataBaseOverView'),
]