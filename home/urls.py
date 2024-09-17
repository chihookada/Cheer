from django.urls import path
from . import views

urlpatterns = [
    path('', views.go_home, name="home"),
    path('history/', views.go_history, name="history"),
    path('favorite/', views.go_favorite, name="favorite"),
    path('settings/', views.go_settings, name="settings")
]