# Generated by Django 3.2 on 2021-04-25 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grapher', '0003_cachetoptickersliteralposts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cachecommentsentiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('text_blob', models.FloatField(blank=True, null=True)),
                ('vader', models.FloatField(blank=True, null=True)),
                ('flair', models.FloatField(blank=True, null=True)),
                ('sentiment', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'CacheCommentSentiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cacheextractionliteral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('mentions', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'CacheExtractionLiteral',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cacheextractionnoun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('mentions', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'CacheExtractionNoun',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cachetoptickersliteral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('subreddit', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'CacheTopTickersLiteral',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cachetoptickersnoun',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('subreddit', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'CacheTopTickersNoun',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cachetoptickersnounpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('subreddit', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'CacheTopTickersNounPost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cachetoptickerssentiment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('sentiment', models.FloatField(blank=True, null=True)),
                ('subreddit', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'CacheTopTickersSentiment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cachetoptickerssentimentpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.CharField(blank=True, max_length=255, null=True)),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('sentiment', models.FloatField(blank=True, null=True)),
                ('subreddit', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'CacheTopTickersSentimentPost',
                'managed': False,
            },
        ),
    ]