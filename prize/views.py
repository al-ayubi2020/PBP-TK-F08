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
def index_redeemed(request):
    user = request.user
    role = get_user_roles(user)
    if(has_role(user, commonUser)):
        return render(request, 'index_redeemed_prize.html')
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
            check_prize = RedeemedPrize.objects.filter(user=user, nama=prize.nama).first()
            if prize.stok > 0: # Stok harus ada
                if (userdata.poin >= prize.poin): # Poin harus cukup
                    if(check_prize == None): # Berarti ini prize baru yang di-redeem sama user
                        redeemedprize = RedeemedPrize(
                            nama=prize.nama,
                            user=user,
                            desc=prize.desc
                        )
                        redeemedprize.save()
                    else: # Berarti jenis prize ini udah pernah di-redeem sama user, kita cuma perlu update stok-nya aja
                        redeemedprize = RedeemedPrize.objects.get(user=user, nama=prize.nama)
                        redeemedprize.stok += 1
                        redeemedprize.save()

                    prize.stok -= 1 # Set stok prize setelah redeem
                    prize.save()

                    userdata.poin -= prize.poin # Kurangi poin user setelah redeem
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
            redeemedprize = RedeemedPrize.objects.get(user=user, pk=id) # Search redeemed prize
            if redeemedprize.stok == 1: # If there's only 1 prize, it will be deleted from database
                redeemedprize.delete()
            else: # Stok redeemed prize lebih dari 1, berarti saat digunakan stok-nya akan berkurang
                redeemedprize.stok -= 1
                redeemedprize.save()
            return JsonResponse({"instance": "Prize berhasil digunakan"}, status=200) 
        return redirect('prize:index')
    return redirect('/login/')