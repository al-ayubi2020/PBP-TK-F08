from django.urls import path
from .views import index
from .views import login_user
from .views import logout_user
from .views import register

app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
]