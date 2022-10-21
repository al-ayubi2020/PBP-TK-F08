from django.urls import path, include
from .views import index

app_name = 'user_dashboard'

urlpatterns = [
    path('', index, name='index'),
]