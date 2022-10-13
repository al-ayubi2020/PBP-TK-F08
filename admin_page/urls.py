from django.urls import path
from .views import index

app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
]