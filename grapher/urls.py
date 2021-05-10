from django.urls import path

from . import views

app_name = 'grapher'
urlpatterns = [
    # path('SubredditLiteralBar', views.SubredditLiteralBarView.as_view(),name='SubredditLiteralBar'), 
    path('Sentiment/', views.SentimentView.as_view(), name='SentimentView'),
    path('Sentiment/<str:sortby>', views.SentimentView.as_view(), name='SentimentView'),
    path('Sentiment/<int:bars>/<int:days>/<str:subreddits>/<str:sortby>', views.SentimentView.as_view(), name='SentimentView'),
    path('Sentiment/<int:bars>/<int:days>/<str:subreddits>', views.SentimentView.as_view(), name='SentimentView'),
    path('Sentiment/<int:bars>/<int:days>/<str:subreddits>/<str:sortby>', views.SentimentView.as_view(), name='SentimentView'),

    path('SingleSentiment/<str:ticker>', views.SingleSenitmentView.as_view(), name='SingleSentiment'),
    path('SingleSentiment/<int:bars>/<int:days>/<str:subreddits>/<str:ticker>', views.SingleSenitmentView.as_view(), name='SingleSentiment'),
    
    
    path('NounView/',views.NounView.as_view(),name='NounView'),
    path('NounView/<int:bars>/<int:days>/<str:subreddits>',views.NounView.as_view(),name='NounView'),
 

    path('LiteralView/',views.LiteralView.as_view(),name='LiteralView'),
    path('LiteralView/<str:ticker>',views.SingleSenitmentView.as_view(),name='SingleSenitment'),
    path('LiteralView/<int:bars>/<int:days>/<str:subreddits>',views.LiteralView.as_view(),name='LiteralView'),
    path('LiteralView/<int:bars>/<int:days>/<str:subreddits>/<str:ticker>',views.LiteralView.as_view(),name='LiteralView'),
    
    path('BubbleSentimentView/',views.BubbleSentimentView.as_view(),name='BubbleSentimentView'),
    path('BubbleSentimentView/<str:ticker>',views.SingleSenitmentView.as_view(),name='SingleSentiment'),
    path('BubbleSentimentView/<int:bars>/<int:days>/<str:subreddits>',views.BubbleSentimentView.as_view(),name='BubbleSentimentView'),
    path('BubbleSentimentView/<int:bars>/<int:days>/<str:subreddits>/<str:sortby>',views.BubbleSentimentView.as_view(),name='BubbleSentimentView'),


    path('SentimentTreeView/',views.SentimentTreeView.as_view(),name='SentimentTreeView'),
    path('SentimentTreeView/<str:ticker>', views.SingleSenitmentView.as_view(), name='SingleSentiment'),
    path('SentimentTreeView/<int:bars>/<int:days>/<str:subreddits>',views.SentimentTreeView.as_view(),name='SentimentTreeView'),
    path('SentimentTreeView/<int:bars>/<int:days>/<str:subreddits>/<str:ticker>',views.SentimentTreeView.as_view(),name='SentimentTreeView'),
    path('SentimentTreeView/<int:bars>/<int:days>/<str:subreddits>/<str:sortby>/<str:ticker>',views.SingleSenitmentView.as_view(),name='SentimentTreeView'),
    # path('SubredditLiteralBarWatchList/<str:view_watch_list>', views.SubredditLiteralBarView.as_view(),name='SubredditLiteralBarWatchList'),
    # path('SubredditLiteralBarPost/<int:bar_quantity>/<int:days>/<str:subreddit_ids>/<str:view_watch_list>', views.SubredditLiteralBarView.as_view(),name='SubredditLiteralBarPost'),
    # path('SubredditLiteralBarPost/<int:bar_quantity>/<int:days>/<str:subreddit_ids>/<str:view_watch_list>/<str:ticker>', views.SubredditLiteralBarView.as_view(),name='SubredditLiteralBarPost'),
    

    # path('<str:ticker>/<int:days>/<str:subreddit_ids>', views.SingleLiteralTickerView.as_view(), name='singleticker'),
    # path('<str:ticker>/<int:days>/<str:subreddit_ids>/<str:initial_reset>', views.SingleLiteralTickerView.as_view(), name='singletickerreset'),

    
]