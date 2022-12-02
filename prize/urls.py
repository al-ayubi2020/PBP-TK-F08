from django.urls import path
from .views import *

app_name = 'prize'

urlpatterns = [
    path('', index, name='index'),
    path('redeem/', index_redeemed, name='index_redeem'),
    path('json/', get_prize, name="prize"),
    path('redeemjson/', get_prize_redeem , name="redeem"),
    path('redeem/<int:id>/', redeem, name="redeem_prize"),
    path('redeem/useprize/<int:id>/', use, name="use_prize"),
]