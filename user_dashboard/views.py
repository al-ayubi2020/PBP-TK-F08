from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from project_django.roles import commonUser
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.checkers import has_role
from admin_page.models import UserData
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        userdata = UserData.objects.get(user=user)
        return render(request, 'index_user_dashboard.html',{'username': user.username, 'poin': userdata.poin, 'balance': userdata.balance})
    return redirect('/login/')

@login_required(login_url='/login/')
def get_userData(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        userdata = UserData.objects.filter(user=user)
        return HttpResponse(serializers.serialize("json", userdata), content_type="application/json")
    return redirect('/login/')