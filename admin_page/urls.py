from django.urls import path
from .views import index
from .views import index_deposit
from .views import get_deposit
from .views import get_deposit_count
from .views import index_prize
from .views import login_user
from .views import logout_user
from .views import register
from .views import acc_deposit
from .views import del_deposit
from .views import add_deposit
from .views import add_prize
from .views import get_prize
from .views import del_prize


app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
    path('deposit/', index_deposit, name='deposit'),
    path('deposit/get/', get_deposit, name='get_deposit'),
    path('deposit/get/count/', get_deposit_count, name='get_deposit_count'),
    path('deposit/add/', add_deposit, name='add_deposit'),
    path('deposit/del/<int:id>', del_deposit, name='del_deposit'),
    path('deposit/acc/<int:id>', acc_deposit, name='acc_deposit'),
    path('prize/', index_prize, name='prize'),
    path('prize/add', add_prize, name='add_prize'),
    path('prize/get', get_prize, name='get_prize'),
    path('prize/del/<int:id>', del_prize, name='del_prize'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
]