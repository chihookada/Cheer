from django.contrib import admin

# Register your models here.

from .models import Post
# from .models import Post, User_fav

admin.site.register(Post)
# admin.site.register(User_fav)