from django.urls import path
from .views import index
from .views import index_deposit
from .views import index_prize
from .views import index_withdraw
from .views import login_user
from .views import logout_user
from .views import register

app_name = 'admin_page'

urlpatterns = [
    path('', index, name='index'),
    path('withdraw/', index_withdraw, name='withdraw'),
    path('deposit/', index_deposit, name='deposit'),
    path('prize/', index_prize, name='prize'),
    path('login/', login_user, name='login_user'),
    path('register/', register, name='register'),
    path('logout/', logout_user, name='logout_user'),
]