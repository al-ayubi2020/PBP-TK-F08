from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poin = models.IntegerField(default=0)
    balance = models.IntegerField(default=0)