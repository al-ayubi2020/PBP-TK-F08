from django.urls import path, include
from .views import index
from .views import get_userData

app_name = 'user_dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('userData/', get_userData, name='get_userData'),
]