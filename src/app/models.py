from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.


class config(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=500)
    create_time = models.DateTimeField(auto_now=False, default=timezone.now)
    update_time = models.DateTimeField(auto_now=False, default=timezone.now)


class dev_kpi_day(models.Model):
    dev_id = models.CharField(max_length=50)
    collect_time = models.CharField(max_length=50)
    sn = models.CharField(max_length=50)
    installed_capacity = models.FloatField(max_length=50) 
    product_power = models.FloatField(max_length=50)
    perpower_ratio = models.FloatField(max_length=50)
    create_time = models.DateTimeField(auto_now=False, default=timezone.now)
