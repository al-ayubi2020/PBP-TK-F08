from django.db import models
from django.contrib.auth.models import User


class Testimoni(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.TextField(default='')
    desc = models.TextField()