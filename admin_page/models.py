from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Prize(models.Model):
    nama = models.TextField()
    poin = models.IntegerField()
    stok = models.IntegerField()

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    jumlah = models.TextField()
    isApprove = models.TextField()

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now)
    jenisSampah = models.TextField()
    beratSampah = models.IntegerField()
    poin = models.IntegerField()
    totalHarga = models.IntegerField()
    isApprove = models.TextField()

