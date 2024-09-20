from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='login')
def go_home(request):
    return render(request, "home/home.html")

def go_home_guest(request):
    return render(request, "home/home-guest.html")

@login_required(login_url='login')
def go_history(request):
    return render(request, "home/history.html")

@login_required(login_url='login')
def go_favorite(request):
    return render(request, "home/favorite.html")

@login_required(login_url='login')
def go_settings(request):
    return render(request, "home/settings.html")