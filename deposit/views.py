from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from project_django.roles import commonUser
from rolepermissions.roles import assign_role, get_user_roles
from rolepermissions.checkers import has_role
from django.http.response import JsonResponse
from django.core import serializers
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
import math

from deposit.models import Deposit
from admin_page.models import UserData

from .forms import DepositForm

@login_required(login_url='/login/')
def index(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        form = DepositForm()
        context = {
            'form' : form
        }
        return render(request, 'index_deposit.html', context)
    return redirect('/login/')

@login_required(login_url='/login/')
def getDeposit(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        deposit = Deposit.objects.filter(user=user).order_by('-pk')
        return HttpResponse(serializers.serialize("json", deposit), content_type="application/json")
    return redirect('/login/')

@login_required(login_url='/login/')
def add(request):
    user = request.user
    role = get_user_roles(user)
    if has_role(user, commonUser):
        form = DepositForm()
        if request.method == 'POST' and form.is_valid:
            HARGA_PLASTIK = 10000
            HARGA_ELEKTRONIK = 12000
            user = request.user
            jenisSampah = request.POST.get('jenisSampah')
            beratSampah = int(request.POST.get('beratSampah'))
            if (beratSampah > 0):
                totalHarga = 0
                if jenisSampah == "Plastik":
                    totalHarga = beratSampah * HARGA_PLASTIK
                elif jenisSampah == "Elektronik":
                    totalHarga = beratSampah * HARGA_ELEKTRONIK
                poin = totalHarga // 1000
                deposit = Deposit(beratSampah=beratSampah, jenisSampah=jenisSampah, totalHarga=totalHarga, poin=poin, user=user, username=user.username, isApprove="PENDING")
                deposit.save()
                return JsonResponse({"instance": "Deposit Diajukan"}, status=200) 
            return JsonResponse({"instance": "Input tidak valid"}, status=200) 
        return redirect('deposit:index')
    return redirect('/login/')