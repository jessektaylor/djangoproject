from django.db import models

# Create your models here.
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