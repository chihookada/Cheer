from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.go_home, name="home"),
    path('guest', views.go_home_guest, name="home_guest"),
    path('history/', views.go_history, name="history"),
    path('favorite/', views.go_favorite, name="favorite"),
    path('settings/', views.go_settings, name="settings"),
    path('delete-p/', views.delete_post, name="delete_post"),
    path('delete-f/', views.delete_fav, name="delete_fav"),
    path('post/', include('post.urls')),
    path('auth/', include('login.urls')),
    path("i18n/", include("django.conf.urls.i18n")),
]