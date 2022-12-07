from django.urls import path
from .views import *

app_name = 'flutter'

urlpatterns = [

    # auth
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout_user, name='logout_user'),

    # admin
    path('admin/username/get/', admin_get_username, name='admin_get_username'),
    path('admin/deposit/get/', admin_get_deposit, name='admin_get_deposit'),
    path('admin/deposit/count/', admin_get_deposit_count, name='admin_get_deposit_count'),
    path('admin/deposit/add/', admin_add_deposit, name='admin_add_deposit'),
    path('admin/deposit/acc/', admin_acc_deposit, name='admin_acc_deposit'),
    path('admin/deposit/del/', admin_del_deposit, name='admin_del_deposit'),
    path('admin/prize/get/', admin_get_prize, name='admin_get_prize'),
    path('admin/prize/add/', admin_add_prize, name='admin_add_prize'),
    path('admin/prize/del/', admin_del_prize, name='admin_del_prize'),
    
    # user
    path('user/data/get/', user_get_data, name='user_get_data'),
    path('user/prize/get/', user_get_prize, name='user_get_prize'),
    path('user/prize/redeem/get/', user_get_prize_redeem, name='user_get_prize_redeem'),
    path('user/prize/redeem/', user_redeem_prize, name='user_redeem_prize'),
    path('user/prize/redeem/use/', user_use_prize, name='user_use_prize'),
    path('user/withdraw/get/', user_get_withdraw, name='user_get_withdraw'),
    path('user/withdraw/add/', user_add_withdraw, name='user_add_withdraw'),
    path('user/deposit/get/', user_get_deposit, name='user_get_deposit'),
    path('user/deposit/add/', user_add_deposit, name='user_add_deposit'),
    path('user/testimoni/add/', user_add_testimoni, name='user_add_testimoni'),
    
    # all
    path('testimoni/get/', get_testimoni, name='get_testimoni'),
    path('is-user/', get_is_user, name='get_is_user'),
]