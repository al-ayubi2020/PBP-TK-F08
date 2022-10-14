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

def index(request):
    isLogin = str(request.user)
    if (isLogin == 'AnonymousUser'):
        return render(request, 'index_landing.html', {'isLogin': False})
    return render(request, 'index_landing.html', {'isLogin': True})

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
                    messages.success(request, 'Akun telah berhasil dibuat!')
                    return redirect('landing_page:login')
                else:
                    messages.success(request, 'Terjadi masalah!')
            except:
                messages.success(request, 'Username sudah pernah digunakan!')
        else:
            messages.success(request, 'Tidak boleh kosong!')

    
    context = {}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user) 
            response = HttpResponseRedirect(reverse("user_dashboard:index")) 
            return response
        else:
            messages.info(request, 'Username atau Password salah!')
    context = {}
    return render(request, "login.html", context)

@login_required(login_url='/todolist/login/')
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('landing_page:index'))
    return response