from django.db import models

# Create your models here.
class Redditcomment(models.Model):
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    commentusername = models.CharField(max_length=255)
    upvotes = models.IntegerField(blank=True, null=True)
    commenttext = models.CharField(max_length=3000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'redditcomment'
    
class Redditpost(models.Model):
    title = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    upvotes = models.IntegerField()
    percentupvotes = models.IntegerField()
    commentquanity = models.IntegerField()
    posttext = models.CharField(max_length=3000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'redditpost'

class Redditsubreddit(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'redditsubreddit'
    
    def __str__(self):
        return self.subreddit
    