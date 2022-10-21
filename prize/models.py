from django.db import models
from django.contrib.auth.models import User
from admin_page.models import Prize
# Create your models here.

class RedeemedPrize(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nama = models.ForeignKey(Prize, on_delete=models.CASCADE)