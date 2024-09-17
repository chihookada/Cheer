from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def go_home(request):
    return render(request, "home/home.html")

def go_history(request):
    return render(request, "home/history.html")

def go_favorite(request):
    return render(request, "home/favorite.html")

def go_settings(request):
    return render(request, "home/settings.html")