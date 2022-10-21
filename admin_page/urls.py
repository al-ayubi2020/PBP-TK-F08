from django.urls import path
from .views import index
from .views import index_deposit
from .views import get_deposit
from .views import index_prize
from .views import login_user
from .views import logout_user
from .views import register
from .views import acc_deposit

app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
    path('deposit/', index_deposit, name='deposit'),
    path('deposit/get/', get_deposit, name='get_deposit'),
    path('deposit/acc/<int:id>', acc_deposit, name='acc_deposit'),
    path('prize/', index_prize, name='prize'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
]