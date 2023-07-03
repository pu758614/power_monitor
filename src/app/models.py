from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class config(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=500)
    create_time = models.DateTimeField( auto_now=False,default=timezone.now)
    update_time = models.DateTimeField(auto_now=False,default=timezone.now)