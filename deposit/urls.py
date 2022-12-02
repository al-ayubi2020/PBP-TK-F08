from django.urls import path
from .views import *

app_name = 'deposit'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('get/', getDeposit, name='getDeposit'),
]