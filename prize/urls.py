from django.urls import path
from .views import index
from .views import index_redeemed
from .views import redeem
from .views import get_prize
from .views import get_prize_redeem
from .views import use

app_name = 'prize'

urlpatterns = [
    path('', index, name='index'),
    path('redeem/', index_redeemed, name='index_redeem'),
    path('json/', get_prize, name="prize"),
    path('redeemjson/', get_prize_redeem , name="redeem"),
    path('redeem/<int:id>/', redeem, name="redeem_prize"),
    path('redeem/useprize/<int:id>/', use, name="use_prize"),
]