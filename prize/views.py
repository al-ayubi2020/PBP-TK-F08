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

from admin_page.models import Prize
from .models import RedeemedPrize
from admin_page.models import UserData


@login_required(login_url='/login/')
def index(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        return render(request, 'index_prize.html')
    return redirect('/login/')

@login_required(login_url='/login/')
def get_prize(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        prize = Prize.objects.all().order_by('-pk')
        return HttpResponse(serializers.serialize("json", prize), content_type="application/json")
    return redirect('/login/')

@login_required(login_url='/login/')
def get_prize_redeem(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        prize = RedeemedPrize.objects.filter(user=user).order_by('-pk')
        return HttpResponse(serializers.serialize("json", prize), content_type="application/json")
    return redirect('/login/')

@login_required(login_url='/login/')
def redeem(request, id):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        if request.method == 'POST':
            prize = Prize.objects.get(pk=id)
            userdata = UserData.objects.get(user=user)
            if prize.stok > 0:
                if (userdata.poin >= prize.poin):
                    redeemedprize = RedeemedPrize(nama=prize.nama, user=user, desc=prize.desc)
                    redeemedprize.save()
                    prize.stok -= 1
                    prize.save()
                    userdata.poin -= prize.poin
                    userdata.save()
                    return JsonResponse({"instance": "Berhasil Redeem"}, status=200) 
                return JsonResponse({"instance": "Poin Kurang"}, status=200) 
            return JsonResponse({"instance": "Stok Habis"}, status=200) 
        return redirect('prize:index')
    return redirect('/login/')

@login_required(login_url='/login/')
def use(request, id):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        if request.method == 'POST':
            redeemedprize = RedeemedPrize.objects.get(pk=id)
            if redeemedprize.user == user:
                redeemedprize.delete()
                return JsonResponse({"instance": "Berhasil Digunakan"}, status=200) 
            return JsonResponse({"instance": "User Tidak Sesuai"}, status=200) 
        return redirect('prize:index')
    return redirect('/login/')