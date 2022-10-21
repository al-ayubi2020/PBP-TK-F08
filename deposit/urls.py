from django.urls import path
from .views import index
from .views import getDeposit
from .views import getPending
from .views import add

app_name = 'deposit'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('get/pending/', getPending, name='getPending'),
    path('get/deposit/', getDeposit, name='getDeposit'),
]