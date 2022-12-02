# import django utils
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core import serializers
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

# import role utils
from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser
from rolepermissions.checkers import has_role

# import models
from django.contrib.auth.models import User
from deposit.models import Deposit
from admin_page.models import Prize, UserData

# import forms
from .forms import *

@login_required(login_url='/admin/login/')
def index(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        jumlahUser = UserData.objects.all().count()
        jumlahDeposit = Deposit.objects.all().count()
        return render(request, 'index_admin.html', {'isLogin': True, 'role':role, "jumlahUser" : jumlahUser, 'jumlahDeposit':jumlahDeposit})
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def index_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        form = DepositForm()
        users = UserData.objects.all()
        return render(request, 'index_deposit_admin.html', {'isLogin': True, 'role':role, "users": users, 'form': form})
    return redirect('/admin/login/')


@login_required(login_url='/admin/login/')
def get_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        pending = Deposit.objects.filter(isApprove="PENDING").order_by('-pk')
        return HttpResponse(serializers.serialize("json", pending), content_type="application/json")
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def get_deposit_count(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        pending = Deposit.objects.filter(isApprove="PENDING").count()
        tes = [pending]
        return HttpResponse(tes)
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def add_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        form = DepositForm()
        if request.method == 'POST' and form.is_valid:
            HARGA_PLASTIK = 10000
            HARGA_ELEKTRONIK = 12000
            user = request.POST.get('user')
            jenisSampah = request.POST.get('jenisSampah')
            beratSampah = int(request.POST.get('beratSampah'))
            if (beratSampah > 0):
                userNow = User.objects.get(username=user)
                totalHarga = 0
                if jenisSampah == "Plastik":
                    totalHarga = beratSampah * HARGA_PLASTIK
                elif jenisSampah == "Elektronik":
                    totalHarga = beratSampah * HARGA_ELEKTRONIK
                poin = totalHarga // 1000
                deposit = Deposit(beratSampah=beratSampah, jenisSampah=jenisSampah, totalHarga=totalHarga, poin=poin, user=userNow, username=userNow.username, isApprove="DITERIMA")
                deposit.save()
                userdata = UserData.objects.get(user=userNow)
                userdata.poin += poin
                userdata.balance += totalHarga
                userdata.save()
                return JsonResponse({"instance": "Deposit diajukan"}, status=200) 
            return JsonResponse({"instance": "Input tidak valid"}, status=200) 
        return redirect('admin_page:deposit')
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def acc_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            idx = int(request.POST.get('id'))
            deposit = Deposit.objects.get(pk=idx)
            deposit.isApprove = "DITERIMA"
            deposit.save()
            userdata = UserData.objects.get(user=deposit.user)
            userdata.balance += deposit.totalHarga
            userdata.poin += deposit.poin
            userdata.save()
            return JsonResponse({"instance": "Deposit Diterima"}, status=200) 
        return redirect('admin_page:deposit')
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def del_deposit2(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            idx = int(request.POST.get('id'))
            deposit = Deposit.objects.get(pk=idx)
            deposit.isApprove = "DITOLAK"
            deposit.save()
            return JsonResponse({"instance": "Deposit Dihapus"}, status=200) 
        return redirect('admin_page:deposit')
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def index_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        form = PrizeForm()
        return render(request, 'index_prize_admin.html', {'isLogin': True, 'role':role, 'form': form})
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def add_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        form = PrizeForm()
        if request.method == 'POST' and form.is_valid:
            nama = request.POST.get('nama')
            poin = int(request.POST.get('poin'))
            stok = int(request.POST.get('stok'))
            desc = request.POST.get('desc')
            if (poin > 0 and stok > 0):
                prize = Prize(nama=nama, poin=poin, stok=stok, desc=desc)
                prize.save()
                return JsonResponse({"instance": "Prize Dibuat"}, status=200) 
            return JsonResponse({"instance": "Poin dan Stok tidak boleh 0"}, status=200) 
        return redirect('admin_page:prize')
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def get_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        prize = Prize.objects.all().order_by('-pk')
        return HttpResponse(serializers.serialize("json", prize), content_type="application/json")
    return redirect('/admin/login/')

@login_required(login_url='/admin/login/')
def del_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            idx = int(request.POST.get('id'))
            prize = Prize.objects.get(pk=idx)
            prize.delete()
            return JsonResponse({"instance": "Deposit Diterima"}, status=200) 
        return redirect('admin_page:prize')
    return redirect('/admin/login/')

def register(request):
    form = RegisterForm()
    if request.method == "POST" and form.is_valid:
        username = request.POST.get('username')
        password = request.POST.get('password')
        form = RegisterForm(request.POST)
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

    context = {'form' : form}
    return render(request, 'register_admin.html', context)

def login_user(request):
    form = LoginForm()
    if request.method == 'POST' and form.is_valid:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and has_role(user, superUser):
            login(request, user) 
            response = HttpResponseRedirect(reverse("admin_page:index")) 
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {'form': form}
    return render(request, "login_admin.html", context)

@login_required(login_url='/admin/login/')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('landing_page:index'))
    return response
