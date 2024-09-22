from django.contrib import admin

# Register your models here.
from .models import Post, History

admin.site.register(Post)
admin.site.register(History)