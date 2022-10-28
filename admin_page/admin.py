from django.contrib import admin
from .models import Prize
from admin_page.models import UserData
# Register your models here.

admin.site.register(Prize)
admin.site.register(UserData)