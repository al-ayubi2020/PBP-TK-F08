from django.urls import path
from .views import index
from .views import redeem
from .views import get_prize
from .views import get_prize_redeem
from .views import use

app_name = 'prize'

urlpatterns = [
    path('', index, name='index'),
    path('get_prize/', get_prize, name='get_prize'),
    path('get_prize_redeem/', get_prize_redeem, name='get_prize_redeem'),
    path('redeem/<int:id>', redeem, name='redeem'),
    path('use/<int:id>', use, name='use'),
]