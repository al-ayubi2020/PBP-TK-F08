from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class PendingWithdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    jumlah = models.BigIntegerField()
    isApprove = models.TextField(default="PENDING")