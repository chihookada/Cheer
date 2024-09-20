from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout


# Create your views here.
def register_page(request):
    form = UserCreationForm()
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # what kind of error 
            messages.error(request, "エラーが発生しました。もう一度お試しください。")
            
    return render(request, "login/login-register.html", {'form': form})

def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    context = {}
    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, '未登録のユーザーです')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else: messages.error(request, 'ユーザーネームかパスワードが間違っています')

    context = {'page': page}
    return render(request, "login/login-register.html", context)

def logout_user(request):
    logout(request)
    return redirect('home_guest')