from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.

class config(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=128)
    create_time = models.DateTimeField( auto_now=False)
    update_time = models.DateTimeField(default=timezone.now)