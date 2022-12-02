from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Withdraw(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.now())
    jumlah = models.TextField()
    isApprove = models.TextField(default="APPROVED")