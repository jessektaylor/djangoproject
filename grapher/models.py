from django.db import models
from django.conf import settings
from django.utils import timezone

class Cryptoticker(models.Model):
    id = models.AutoField(primary_key=True)
    ticker = models.CharField(max_length=6)
    crypto_name = models.CharField(max_length=30)
    marketcap = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cryptoticker'
        
class Redditcomment(models.Model):
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    commentusername = models.CharField(max_length=255)
    upvotes = models.IntegerField(blank=True, null=True)
    commenttext = models.CharField(max_length=3000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditcomment'


class Redditcommentcache(models.Model):
    comment_tickers_used = models.CharField(max_length=30000)
    comment_polarity = models.FloatField()
    comment_subjectivity = models.FloatField()
    datetime = models.DateTimeField()
    subreddit = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'redditcommentcache'


class redditcommentliteralextraction(models.Model):
    commentid = models.ForeignKey(Redditcomment, models.DO_NOTHING, db_column='commentid', blank=True, null=True)
    comment_tickers_used = models.CharField(max_length=3000)
    comment_polarity = models.FloatField()
    comment_subjectivity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'redditcommentliteralextraction'


class Redditpost(models.Model):
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    upvotes = models.IntegerField()
    percentupvotes = models.IntegerField()
    commentquanity = models.IntegerField()
    posttext = models.CharField(max_length=3000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditpost'


class Redditpostcache(models.Model):
    id = models.AutoField(primary_key=True)
    title_tickers_used = models.CharField(max_length=300000)
    text_tickers_used = models.CharField(max_length=300000)
    post_title_polarity = models.FloatField()
    post_title_subjectivity = models.FloatField()
    post_text_polarity = models.FloatField()
    post_text_subjectivity = models.FloatField()
    datetime = models.DateTimeField()
    subreddit = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'redditpostcache'


class redditpostliteralextraction(models.Model):
    postid = models.OneToOneField(Redditpost, models.DO_NOTHING, db_column='postid', 
blank=True, null=True)
    id = models.AutoField(primary_key=True)
    title_tickers_used = models.CharField(max_length=300000)
    text_tickers_used = models.CharField(max_length=300000)
    post_title_polarity = models.FloatField()
    post_title_subjectivity = models.FloatField()
    post_text_polarity = models.FloatField()
    post_text_subjectivity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'redditpostliteralextraction'


class Redditsubreddit(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'redditsubreddit'
    
    def __str__(self):
        return self.subreddit
    

