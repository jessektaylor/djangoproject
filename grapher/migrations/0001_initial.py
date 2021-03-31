# Generated by Django 3.1.7 on 2021-03-31 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cryptoticker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ticker', models.CharField(max_length=6)),
                ('crypto_name', models.CharField(max_length=30)),
                ('marketcap', models.FloatField()),
            ],
            options={
                'db_table': 'cryptoticker',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Redditcomment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentusername', models.CharField(max_length=255)),
                ('upvotes', models.IntegerField(blank=True, null=True)),
                ('commenttext', models.CharField(blank=True, max_length=3000, null=True)),
                ('datetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'redditcomment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Redditcommentcache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_tickers_used', models.CharField(max_length=30000)),
                ('comment_polarity', models.FloatField()),
                ('comment_subjectivity', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('subreddit', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'redditcommentcache',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='redditcommentliteralextraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_tickers_used', models.CharField(max_length=3000)),
                ('comment_polarity', models.FloatField()),
                ('comment_subjectivity', models.FloatField()),
            ],
            options={
                'db_table': 'redditcommentliteralextraction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Redditpost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('upvotes', models.IntegerField()),
                ('percentupvotes', models.IntegerField()),
                ('commentquanity', models.IntegerField()),
                ('posttext', models.CharField(blank=True, max_length=3000, null=True)),
                ('datetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'redditpost',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Redditpostcache',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title_tickers_used', models.CharField(max_length=3000)),
                ('title_company_names', models.CharField(max_length=3000)),
                ('text_tickers_used', models.CharField(max_length=3000)),
                ('text_company_names', models.CharField(max_length=3000)),
                ('post_title_polarity', models.FloatField()),
                ('post_title_subjectivity', models.FloatField()),
                ('post_text_polarity', models.FloatField()),
                ('post_text_subjectivity', models.FloatField()),
                ('datetime', models.DateTimeField()),
                ('subreddit', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'redditpostcache',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='redditpostliteralextraction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title_tickers_used', models.CharField(max_length=3000)),
                ('title_company_names', models.CharField(max_length=3000)),
                ('text_tickers_used', models.CharField(max_length=3000)),
                ('text_company_names', models.CharField(max_length=3000)),
                ('post_title_polarity', models.FloatField()),
                ('post_title_subjectivity', models.FloatField()),
                ('post_text_polarity', models.FloatField()),
                ('post_text_subjectivity', models.FloatField()),
            ],
            options={
                'db_table': 'redditpostliteralextraction',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Redditsubreddit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('subreddit', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'redditsubreddit',
                'managed': False,
            },
        ),
    ]