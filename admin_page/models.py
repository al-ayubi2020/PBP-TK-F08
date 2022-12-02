from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Prize(models.Model):
    nama = models.TextField()
    poin = models.BigIntegerField()
    stok = models.BigIntegerField()
    desc = models.TextField(default="")

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.TextField(default="")
    poin = models.BigIntegerField(default=0)
    balance = models.BigIntegerField(default=0)