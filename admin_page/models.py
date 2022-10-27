from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Prize(models.Model):
    nama = models.TextField()
    poin = models.BigIntegerField()
    stok = models.BigIntegerField()
    desc = models.TextField(default="")