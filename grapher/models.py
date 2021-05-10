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


class Tickers(models.Model):
    ticker = models.CharField(primary_key=True, max_length=15)
    exchange = models.CharField(max_length=50)
    type = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Tickers'


class Redditcomment(models.Model):
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    commentusername = models.CharField(max_length=255)
    upvotes = models.IntegerField(blank=True, null=True)
    commenttext = models.CharField(max_length=3000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.ForeignKey('RedditSubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

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
    postid = models.OneToOneField(Redditpost, models.DO_NOTHING, db_column='postid', blank=True, null=True)
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

    subreddit = models.CharField(primary_key=True, unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'redditsubreddit'
       
    def __str__(self):
        return self.subreddit
    

class Nysetickers(models.Model):
    ticker = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    exchange = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'nysetickers'


class Nasdaqtickers(models.Model):
    ticker = models.CharField(max_length=15)
    company_name = models.CharField(max_length=100)
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    volume = models.FloatField()
    exchange = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'nasdaqtickers'


class CheckpointComment(models.Model):
    subreddit = models.CharField(unique=True, max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CheckPointComment'


class CheckpointPost(models.Model):
    subreddit = models.CharField(unique=True, max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CheckPointPost'


class CommentSentiment(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    commentid = models.ForeignKey('Redditcomment', models.DO_NOTHING, db_column='commentid', blank=True, null=True)
    text_blob = models.FloatField(blank=True, null=True)
    vader = models.FloatField(blank=True, null=True)
    flair = models.FloatField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CommentSentiment'
        unique_together = (('subreddit', 'commentid'),)


class ExtractionLiteral(models.Model):
    id = models.AutoField(primary_key=True)
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)  
    commentid = models.ForeignKey('Redditcomment', models.DO_NOTHING, db_column='commentid', blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ExtractionLiteral'
        unique_together = (('subreddit', 'ticker', 'commentid'),)


class ExtractionLiteralPost(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)  
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    mentions_title = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ExtractionLiteralPost'
        unique_together = (('subreddit', 'ticker', 'postid'),)


class ExtractionNoun(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)  
    commentid = models.ForeignKey('Redditcomment', models.DO_NOTHING, db_column='commentid', blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ExtractionNoun'
        unique_together = (('subreddit', 'ticker', 'commentid'),)


class ExtractionNounPost(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)  
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    mentions_title = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ExtractionNounPost'
        unique_together = (('subreddit', 'ticker', 'postid'),)


class PostSentiment(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    text_blob_title = models.FloatField(blank=True, null=True)
    vader_title = models.FloatField(blank=True, null=True)
    flair_title = models.FloatField(blank=True, null=True)
    sentiment_title = models.FloatField(blank=True, null=True)
    text_blob = models.FloatField(blank=True, null=True)
    vader = models.FloatField(blank=True, null=True)
    flair = models.FloatField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'PostSentiment'
        unique_together = (('subreddit', 'postid'),)



class Cachecommentsentiment(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    text_blob = models.FloatField(blank=True, null=True)
    vader = models.FloatField(blank=True, null=True)
    flair = models.FloatField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheCommentSentiment'


class Cacheextractionliteral(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheExtractionLiteral'


class Cacheextractionliteralpost(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    mentions_title = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheExtractionLiteralPost'


class Cacheextractionnoun(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheExtractionNoun'


class Cacheextractionnounpost(models.Model):
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    mentions = models.IntegerField(blank=True, null=True)
    mentions_title = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheExtractionNounPost'


class Cachepostsentiment(models.Model):
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CachePostSentiment'


class Cachetoptickersliteral(models.Model):
    ticker = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheTopTickersLiteral'
        unique_together = (('ticker', 'subreddit', 'datetime'),)


class Cachetoptickersliteralposts(models.Model):
    ticker = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheTopTickersLiteralPosts'
        unique_together = (('ticker', 'subreddit', 'datetime'),)


class Cachetoptickersnoun(models.Model):
    ticker = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheTopTickersNoun'
        unique_together = (('ticker', 'subreddit', 'datetime'),)


class Cachetoptickersnounpost(models.Model):
    ticker = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheTopTickersNounPost'
        unique_together = (('ticker', 'subreddit', 'datetime'),)


class Cachetoptickerssentiment(models.Model):
    ticker = models.CharField(max_length=255, blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheTopTickersSentiment'
        unique_together = (('ticker', 'subreddit', 'datetime'),)


class Cachetoptickerssentimentpost(models.Model):
    ticker = models.CharField(max_length=255, blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    count = models.IntegerField(blank=True, null=True)
    sentiment = models.FloatField(blank=True, null=True)
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'CacheTopTickersSentimentPost'
        unique_together = (('ticker', 'datetime', 'subreddit'),)


class Historicalyahoo(models.Model):
    ticker = models.ForeignKey('Tickers', models.DO_NOTHING, db_column='ticker', blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    open = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)
    close = models.FloatField(blank=True, null=True)
    adjclose = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HistoricalYahoo'
        unique_together = (('ticker', 'datetime'),)