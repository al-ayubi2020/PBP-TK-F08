from django.shortcuts import render

def index(request):
    return render(request, 'index_user_dashboard.html')