from django.urls import path
from .views import *

app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
    path('deposit/', index_deposit, name='deposit'),
    path('deposit/get/', get_deposit, name='get_deposit'),
    path('deposit/get/count/', get_deposit_count, name='get_deposit_count'),
    path('deposit/add/', add_deposit, name='add_deposit'),
    path('deposit/del/', del_deposit2, name='del_deposit2'),
    path('deposit/acc/', acc_deposit, name='acc_deposit'),
    path('prize/', index_prize, name='prize'),
    path('prize/add', add_prize, name='add_prize'),
    path('prize/get', get_prize, name='get_prize'),
    path('prize/del/', del_prize, name='del_prize'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
]