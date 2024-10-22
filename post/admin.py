from django.contrib import admin

# Register your models here.
from .models import Post, History, Evaluation

admin.site.register(Post)
admin.site.register(History)
admin.site.register(Evaluation)