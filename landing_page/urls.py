from django.urls import path
from .views import index
from .views import register
from .views import login_user
from .views import logout_user
from .views import add_testimoni
from .views import get_testimoni

app_name = 'landing_page'

urlpatterns = [
    path('', index, name='index'),
    path('testimoni/add/', add_testimoni, name='add_testimoni'),
    path('testimoni/get/', get_testimoni, name='get_testimoni'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]