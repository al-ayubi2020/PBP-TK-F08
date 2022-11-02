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
from admin_page.models import UserData
from rolepermissions.checkers import has_role

from rolepermissions.roles import assign_role, get_user_roles
from project_django.roles import commonUser

from .forms import LoginForm, RegisterForm, TestimoniForm
from .models import Testimoni

def index(request):
    isLogin = str(request.user)
    user = request.user
    role = get_user_roles(user)
    form = TestimoniForm()
    if (isLogin == 'AnonymousUser'):
        return render(request, 'index_landing.html', {'isLogin': False, 'form':form})
    return render(request, 'index_landing.html', {'isLogin': True, 'role':role, 'form':form})

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
                    userdata = UserData.objects.create(user=acc)
                    assign_role(acc, commonUser)
                    messages.success(request, 'Akun telah berhasil dibuat!')
                    return redirect('landing_page:login')
                else:
                    messages.success(request, 'Terjadi masalah!')
                    return JsonResponse({"instance": "Ada yang salah"}, status=200)
            except:
                messages.success(request, 'Username sudah pernah digunakan!')
                return JsonResponse({"instance": "Ada yang salah"}, status=200)
        else:
            messages.success(request, 'Tidak boleh kosong!')

    
    context = {'form' : form}
    return render(request, 'register.html', context)

def login_user(request):
    form = LoginForm()
    if request.method == 'POST' and form.is_valid:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and has_role(user, commonUser):
            login(request, user) 
            return HttpResponseRedirect(reverse("user_dashboard:index")) 
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {'form' : form}
    return render(request, "login.html", context)

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('landing_page:index'))
    return response

def get_testimoni(request):
    testi = Testimoni.objects.all().order_by('-pk')[:3]
    return HttpResponse(serializers.serialize("json", testi), content_type="application/json")

@login_required(login_url='/login/')
def add_testimoni(request):
    user = request.user
    role = get_user_roles(user)
    if has_role(user, commonUser):
        form = TestimoniForm()
        if request.method == 'POST' and form.is_valid:
            try:
                testi = Testimoni.objects.filter(user=user).count()
                if testi == 0:
                    desc = request.POST.get('desc')
                    username = User.objects.get(username=user.username)
                    createTesti = Testimoni(desc=desc, user=user, username=username)
                    createTesti.save()
                    return JsonResponse({"instance": "Testimoni dibuat"}, status=200) 
                return JsonResponse({"instance": "Sudah pernah memberikan testimoni"}, status=200) 
            except:
                return JsonResponse({"instance": "Ada yang salah"}, status=200)
        return redirect('landing_page:index')
    return redirect('/login/')
