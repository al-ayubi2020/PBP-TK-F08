from django.urls import path
from .views import index

app_name = 'withdraw'

urlpatterns = [
    path('', index, name='index'),
]