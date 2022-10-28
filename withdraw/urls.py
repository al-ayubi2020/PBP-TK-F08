from django.urls import path
from .views import index
from .views import add
from .views import get

app_name = 'withdraw'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('get/', get, name='get'),
]