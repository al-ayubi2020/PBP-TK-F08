from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class PendingDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    username = models.TextField(default='')
    jenisSampah = models.TextField()
    beratSampah = models.BigIntegerField()
    poin = models.BigIntegerField()
    totalHarga = models.BigIntegerField()
    isApprove = models.TextField(default='PENDING')