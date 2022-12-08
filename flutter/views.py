# import respons util
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse

# import role util
from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import superUser, commonUser
from rolepermissions.checkers import has_role

# imoport model
from django.contrib.auth.models import User
from admin_page.models import Prize, UserData
from deposit.models import Deposit
from landing_page.models import Testimoni
from prize.models import RedeemedPrize
from withdraw.models import Withdraw

# import auth util
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login, logout

@csrf_exempt
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            try:
                acc = User.objects.create(username=username)
                if acc:
                    acc.set_password(password)
                    acc.save()
                    userdata = UserData.objects.create(user=acc)
                    userdata.email = username
                    userdata.save()
                    assign_role(acc, commonUser)
                    return JsonResponse({ "status": 200, "message": "Successfully Register!" }, status=200)
                else:
                    return JsonResponse({ "status": 500, "message": "Terjadi masalah!" }, status=500)
            except:
                return JsonResponse({ "status": 406, "message": "Username sudah pernah digunakan." }, status=406)
        else:
            return JsonResponse({ "status": 400, "message": "username dan password boleh kosong" }, status=400)
    return JsonResponse({"status": 502, "message": "Method not allowed"}, status=502)

@csrf_exempt
def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if (has_role(user, superUser)):
                    return JsonResponse({ "status": 200, "message": "Successfully Logged In!", "role":'admin' }, status=200)
                else:
                    return JsonResponse({ "status": 200, "message": "Successfully Logged In!", "role":'user' }, status=200)
            else:
                return JsonResponse({
                "status": 401,
                "message": "Failed to Login, check your email/password.",
                }, status=401)
        else:
            return JsonResponse({ "status": 400, "message": "username dan password tidak boleh kosong" }, status=400)
    return JsonResponse({"message": "Method not allowed", 'status':502}, status=502)

@csrf_exempt
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "Berhasil logout", 'status':200}, status=200)
    
@csrf_exempt
def admin_get_username(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        pending = UserData.objects.all().order_by('-pk')
        return HttpResponse(serializers.serialize("json", pending), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def admin_get_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        pending = Deposit.objects.filter(isApprove="PENDING").order_by('-pk')
        return HttpResponse(serializers.serialize("json", pending), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def admin_get_deposit_count(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        pending = Deposit.objects.filter(isApprove="PENDING").count()
        tes = [pending]
        return HttpResponse(tes)
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def admin_add_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
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
                return JsonResponse({"message": "Deposit diajukan" ,"status":200}, status=200) 
            return JsonResponse({ "message": "Input tidak valid", "status":400}, status=400)
        return JsonResponse({"message": "Method not allowed", "status":502}, status=502)
    return JsonResponse({ "message": "Belum login!" , "status":403}, status=403)

@csrf_exempt
def admin_acc_deposit(request):
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
            return JsonResponse({"message": "Deposit Diterima", 'status':200}, status=200) 
        return JsonResponse({"message": "Method not allowed", 'status':502}, status=502)
    return JsonResponse({ "message": "Belum login!", 'status':403 }, status=403)

@csrf_exempt
def admin_del_deposit(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            idx = int(request.POST.get('id'))
            deposit = Deposit.objects.get(pk=idx)
            deposit.isApprove = "DITOLAK"
            deposit.save()
            return JsonResponse({"message": "Deposit Dihapus", 'status':200}, status=200) 
        return JsonResponse({"message": "Method not allowed", 'status':502}, status=502)
    return JsonResponse({ "message": "Belum login!" , 'status':403}, status=403)

@csrf_exempt
def admin_add_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            nama = request.POST.get('nama')
            poin = int(request.POST.get('poin'))
            stok = int(request.POST.get('stok'))
            desc = request.POST.get('desc')
            if (poin > 0 and stok > 0):
                prize = Prize(nama=nama, poin=poin, stok=stok, desc=desc)
                prize.save()
                return JsonResponse({"message": "Prize Dibuat", 'status':200}, status=200) 
            return JsonResponse({"message": "Poin dan Stok tidak boleh 0", 'status':200}, status=200) 
        return JsonResponse({"message": "Method not allowed", 'status':502}, status=502)
    return JsonResponse({ "message": "Belum login!" , "status":403}, status=403)

@csrf_exempt
def admin_get_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        prize = Prize.objects.all().order_by('-pk')
        return HttpResponse(serializers.serialize("json", prize), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def admin_del_prize(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, superUser)):
        if request.method == 'POST':
            idx = int(request.POST.get('id'))
            prize = Prize.objects.get(pk=idx)
            prize.delete()
            return JsonResponse({"message": "Deposit Diterima", 'status':200}, status=200) 
        return JsonResponse({"message": "Method not allowed", 'status':502}, status=502)
    return JsonResponse({ "message": "Belum login!", 'status':403}, status=403)

@csrf_exempt
def user_get_prize(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        prize = Prize.objects.all().order_by('-pk')
        return HttpResponse(serializers.serialize("json", prize), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def user_get_prize_redeem(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        prize = RedeemedPrize.objects.filter(user=user).order_by('-pk')
        return HttpResponse(serializers.serialize("json", prize), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def user_redeem_prize(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        if request.method == 'POST':
            itemId = int(request.POST.get('id'))
            prize = Prize.objects.get(pk=itemId)
            check_prize = RedeemedPrize.objects.filter(user=user, nama=prize.nama).first()
            if prize.stok > 0: # Stok harus ada
                userdata = UserData.objects.get(user=user)
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

                    return JsonResponse({"message": "Berhasil Redeem"}, status=200) 
                return JsonResponse({"message": "Poin Kurang"}, status=200) 
            return JsonResponse({"message": "Stok Habis"}, status=200) 
        return JsonResponse({"message": "Method not allowed"}, status=502)
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def user_use_prize(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        if request.method == 'POST':
            try:
                itemId = int(request.POST.get('id'))
                redeemedprize = RedeemedPrize.objects.get(user=user, pk=itemId) # Search redeemed prize
                if redeemedprize.stok == 1: # If there's only 1 prize, it will be deleted from database
                    redeemedprize.delete()
                else: # Stok redeemed prize lebih dari 1, berarti saat digunakan stok-nya akan berkurang
                    redeemedprize.stok -= 1
                    redeemedprize.save()
                return JsonResponse({"message": "Prize berhasil digunakan"}, status=200) 
            except:
                return JsonResponse({"message": "Ada yang salah"}, status=500)
        return JsonResponse({"message": "Method not allowed"}, status=502)
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def user_add_withdraw(request):
    user = request.user
    role = get_user_roles(user)
    if has_role(user, commonUser):
        if request.method == 'POST':
            jumlah = int(request.POST.get('jumlah'))
            userdata = UserData.objects.get(user=user)
            if (jumlah > 0):
                if (userdata.balance >= jumlah):
                    withdraw = Withdraw(jumlah=jumlah, user=user)
                    withdraw.save()
                    userdata.balance -= jumlah
                    userdata.save()
                    return JsonResponse({"message": "Penarikan Berhasil", 'status':200}, status=200) 
                return JsonResponse({"message": "Saldo Kurang", 'status':300}, status=200) 
            return JsonResponse({"message": "Input tidak valid", 'status':300}, status=200) 
        return JsonResponse({"message": "Method not allowed", 'status':502}, status=502)
    return JsonResponse({ "message": "Belum login!" , 'status':403}, status=403)

@csrf_exempt
def user_get_withdraw(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        withdraw = Withdraw.objects.filter(user=user).order_by('-pk')
        return HttpResponse(serializers.serialize("json", withdraw), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def user_get_deposit(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        deposit = Deposit.objects.filter(user=user).order_by('-pk')
        return HttpResponse(serializers.serialize("json", deposit), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def user_add_deposit(request):
    user = request.user
    role = get_user_roles(user)
    if has_role(user, commonUser):
        if request.method == 'POST':
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
                return JsonResponse({"message": "Deposit diajukan" ,"status":200}, status=200) 
            return JsonResponse({ "message": "Input tidak valid", "status":400}, status=400)
        return JsonResponse({"message": "Method not allowed", "status":502}, status=502)
    return JsonResponse({ "message": "Belum login!" , "status":403}, status=403)

@csrf_exempt
def get_testimoni(request):
    testi = Testimoni.objects.all().order_by('-pk')[:3]
    return HttpResponse(serializers.serialize("json", testi), content_type="application/json")

@csrf_exempt
def user_add_testimoni(request):
    user = request.user
    role = get_user_roles(user)
    if has_role(user, commonUser):
        if request.method == 'POST':
            try:
                testi = Testimoni.objects.filter(user=user).count()
                if testi == 0:
                    desc = request.POST.get('desc')
                    username = User.objects.get(username=user.username)
                    createTesti = Testimoni(desc=desc, user=user, username=username)
                    createTesti.save()
                    return JsonResponse({"message": "Testimoni dibuat", 'status':200}, status=200) 
                return JsonResponse({"message": "Sudah pernah memberikan testimoni", 'status':300}, status=200) 
            except:
                return JsonResponse({"message": "Ada yang salah", 'status':500}, status=500)
        return JsonResponse({"message": "Method not allowed", "status":502}, status=502)
    return JsonResponse({ "message": "Belum login atau bukan user!" , "status":403}, status=403)

@csrf_exempt
def user_get_data(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        userdata = UserData.objects.filter(user=user)
        return HttpResponse(serializers.serialize("json", userdata), content_type="application/json")
    return JsonResponse({ "message": "Belum login!" }, status=403)

@csrf_exempt
def get_is_user(request):
    user = request.user
    role = get_user_roles(user)
    if (has_role(user, commonUser)):
        print(user)
        return JsonResponse({ "isUser": "true" }, status=200)
    print(user)
    return JsonResponse({ "isUser": "false" }, status=200)


