from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.go_home, name="home"),
    path('guest', views.go_home_guest, name="home_guest"),
    path('history/', views.go_history, name="history"),
    path('favorite/', views.go_favorite, name="favorite"),
    path('settings/', views.go_settings, name="settings"),
    path('post/', include('post.urls')),
    path('auth/', include('login.urls')),
]