from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class PendingDeposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    jenisSampah = models.TextField()
    beratSampah = models.IntegerField()
    poin = models.IntegerField()
    totalHarga = models.IntegerField()
    isApprove = models.TextField(default='PENDING')