# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cryptoticker(models.Model):
    id = models.AutoField()
    ticker = models.CharField(max_length=6)
    crypto_name = models.CharField(max_length=30)
    marketcap = models.FloatField()

    class Meta:
        managed = False
        db_table = 'cryptoticker'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GrapherRequestedticker(models.Model):
    ticker = models.CharField(primary_key=True, max_length=10)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'grapher_requestedticker'


class Nasdaqtickers(models.Model):
    id = models.AutoField()
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


class Nysetickers(models.Model):
    id = models.AutoField()
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


class Redditcomment(models.Model):
    postid = models.ForeignKey('Redditpost', models.DO_NOTHING, db_column='postid', blank=True, null=True)
    id = models.AutoField()
    commentusername = models.CharField(max_length=255)
    upvotes = models.IntegerField(blank=True, null=True)
    commenttext = models.CharField(max_length=10000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditcomment'


class Redditcommentcache(models.Model):
    id = models.AutoField()
    comment_tickers_used = models.CharField(max_length=300000)
    comment_polarity = models.FloatField()
    comment_subjectivity = models.FloatField()
    datetime = models.DateTimeField()
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditcommentcache'


class Redditcommentliteralextraction(models.Model):
    commentid = models.IntegerField(unique=True, blank=True, null=True)
    comment_tickers_used = models.CharField(max_length=100000)
    comment_polarity = models.FloatField()
    comment_subjectivity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'redditcommentliteralextraction'


class Redditlastcommentupdate(models.Model):
    datetime = models.DateTimeField()
    subreddit = models.OneToOneField('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditlastcommentupdate'


class Redditlastpostupdate(models.Model):
    datetime = models.DateTimeField()
    subreddit = models.OneToOneField('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditlastpostupdate'


class Redditpost(models.Model):
    title = models.CharField(max_length=10000)
    username = models.CharField(max_length=255)
    upvotes = models.IntegerField()
    percentupvotes = models.IntegerField()
    commentquanity = models.IntegerField()
    posttext = models.CharField(max_length=10000, blank=True, null=True)
    datetime = models.DateTimeField()
    subreddit = models.ForeignKey('Redditsubreddit', models.DO_NOTHING, db_column='subreddit', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditpost'


class Redditpostcache(models.Model):
    id = models.AutoField()
    title_tickers_used = models.CharField(max_length=3000)
    text_tickers_used = models.CharField(max_length=3000)
    post_title_polarity = models.FloatField()
    post_title_subjectivity = models.FloatField()
    post_text_polarity = models.FloatField()
    post_text_subjectivity = models.FloatField()
    datetime = models.DateTimeField()
    subreddit = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'redditpostcache'


class Redditpostliteralextraction(models.Model):
    postid = models.OneToOneField(Redditpost, models.DO_NOTHING, db_column='postid', blank=True, null=True)
    title_tickers_used = models.CharField(max_length=100000)
    text_tickers_used = models.CharField(max_length=100000)
    post_title_polarity = models.FloatField()
    post_title_subjectivity = models.FloatField()
    post_text_polarity = models.FloatField()
    post_text_subjectivity = models.FloatField()

    class Meta:
        managed = False
        db_table = 'redditpostliteralextraction'


class Redditsubreddit(models.Model):
    id = models.AutoField()
    subreddit = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'redditsubreddit'
