from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class PendingDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    jenisSampah = models.TextField()
    beratSampah = models.IntegerField()
    poin = models.IntegerField()
    totalHarga = models.IntegerField()
    isApprove = models.TextField(default='PENDING')