# Generated by Django 3.2 on 2021-05-02 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grapher', '0004_cachecommentsentiment_cacheextractionliteral_cacheextractionnoun_cachetoptickersliteral_cachetoptick'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historicalyahoo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('open', models.FloatField(blank=True, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
                ('close', models.FloatField(blank=True, null=True)),
                ('adjclose', models.FloatField(blank=True, null=True)),
                ('volume', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'HistoricalYahoo',
                'managed': False,
            },
        ),
    ]
