from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Post, User_fav

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
