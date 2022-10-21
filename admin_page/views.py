from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http.response import JsonResponse
import datetime

from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser
from rolepermissions.decorators import has_role_decorator
from project_django.roles import superUser
from rolepermissions.checkers import has_role

from deposit.models import PendingDeposit
from .models import Deposit
from landing_page.models import UserData

@login_required(login_url='/admin/login/')
def index(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        return render(request, 'index_admin.html', {'isLogin': True, 'role':role})
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def index_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        return render(request, 'index_deposit_admin.html', {'isLogin': True, 'role':role})
    return redirect('/admin/login/')


@login_required(login_url='/admin/login/')
def get_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        pending = PendingDeposit.objects.all().order_by('-pk')
        return HttpResponse(serializers.serialize("json", pending), content_type="application/json")
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def acc_deposit(request, id):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            pending = PendingDeposit.objects.get(pk=id)
            userNow = User.objects.get(pk=pending.user.id)
            deposit = Deposit(date=pending.date, user=userNow, beratSampah=pending.beratSampah, jenisSampah=pending.jenisSampah, poin=pending.poin, totalHarga=pending.totalHarga, username=userNow.username, isApprove="DITERIMA")
            deposit.save()
            userdata = UserData.objects.get(user=userNow)
            userdata.balance += pending.totalHarga
            userdata.poin += pending.poin
            userdata.save()
            pending.delete()
            return JsonResponse({"instance": "Deposit Diterima"}, status=200) 
        return redirect('admin_page:deposit')
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def index_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        return render(request, 'index_prize_admin.html', {'isLogin': True, 'role':role})
    return redirect('/admin/login/')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = UserCreationForm(request.POST)
        if username and password:
            try:
                acc = User.objects.create(username=username)
                if acc:
                    acc.set_password(password)
                    acc.save()
                    assign_role(acc, superUser)
                    messages.success(request, 'Akun telah berhasil dibuat!')
                    return redirect('admin_page:login_user')
                else:
                    messages.success(request, 'Terjadi masalah!')
            except:
                messages.success(request, 'Username sudah pernah digunakan!')
        else:
            messages.success(request, 'Tidak boleh kosong!')

    
    context = {}
    return render(request, 'register_admin.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = HttpResponseRedirect(reverse("admin_page:index")) 
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, "login_admin.html", context)

@login_required(login_url='/admin/login/')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('landing_page:index'))
    return response