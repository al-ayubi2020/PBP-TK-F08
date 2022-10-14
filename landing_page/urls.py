from django.urls import path
from .views import index
from .views import register
from .views import login_user
from .views import logout_user

app_name = 'landing_page'

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]