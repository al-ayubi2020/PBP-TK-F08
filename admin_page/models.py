from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Prize(models.Model):
    nama = models.TextField()
    poin = models.IntegerField()
    stok = models.IntegerField()

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jumlah = models.TextField()
    isApprove = models.TextField()

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jenisSampah = models.TextField()
    beratSampah = models.IntegerField()
    poin = models.IntegerField()
    totalHarga = models.IntegerField()
    isApprove = models.TextField()

