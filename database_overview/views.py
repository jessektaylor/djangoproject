from django.shortcuts import render
from django.views.generic import View
from . models import Redditcomment, Redditpost, Redditsubreddit
import datetime


# Create your views here.
class DataBaseOverView(View):
    template_name = "database_overview/database_overview.html"
    
    def get(self, request, *args, **kwargs):
        obj = dict()
        # get the number of comments
        obj['comment_count'] = Redditcomment.objects.count()
        # get the number of posts
        obj['post_count'] = Redditpost.objects.count()
        # cycle throug the subreddits and get the number of posts and comments for each
        subreddits = Redditsubreddit.objects.all()
        subreddit_counts = list()
        for subreddit in subreddits:
            sub_comment_count = Redditcomment.objects.filter(subreddit=subreddit.subreddit).count()
            sub_post_count = Redditpost.objects.filter(subreddit=subreddit.subreddit).count()
            temp_list = [sub_post_count + sub_comment_count, subreddit.subreddit]
            subreddit_counts.append(temp_list)
        obj['subreddit_counts'] = subreddit_counts
        print(obj['subreddit_counts'])
        # get last upload date for the most recent post and comment
        obj['last_comment'] = Redditcomment.objects.latest('datetime').datetime 
        obj['last_post'] = Redditpost.objects.latest('datetime').datetime 
        # get how many posts/comments are uploaded each day for last ten days. 
        start_search = datetime.datetime.now()
        total_uploaded_list = list()
        total_uploaded_dates = list()
        for num in range(10):
            com_num = Redditcomment.objects.filter(datetime__range=(
                    start_search - datetime.timedelta(days=1),
                    start_search
                    )).count()
            post_num = Redditpost.objects.filter(datetime__range=(
                    start_search - datetime.timedelta(days=1),
                    start_search
                    )).count()
            total_uploaded = com_num + post_num
            total_uploaded_list.append(total_uploaded)
            total_uploaded_dates.append(start_search.strftime('%d-%b-%Y'))
            start_search = start_search - datetime.timedelta(days=1)
        obj['bar_data'] = total_uploaded_list[::-1]
        obj['bar_labels'] = total_uploaded_dates[::-1]
        obj['oldest_post'] = Redditpost.objects.earliest('datetime').datetime 
        obj['backgroundColor'] = ['rgba(0, 255, 255, 0.8)' for x in range(len(obj['bar_data']))]
        return render(request, self.template_name, obj)
    