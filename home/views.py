from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from post.models import History, Post


# Create your views here.
@login_required(login_url='login')
def go_home(request):
    todays_msg = History.objects.filter(user_id=request.user.id, created_at__date=date.today())
    if todays_msg.exists():
        return redirect('todays-msg')  # Redirect if history exists for today
    return render(request, "home/home.html")

def go_home_guest(request):
    return render(request, "home/home-guest.html")

@login_required(login_url='login')
def go_history(request):
    # user = request.user
    past_posts = Post.objects.filter(user_id=request.user.id).order_by('-created_at')
    # if past_posts == []:
    context = {'past_posts': past_posts }
    # else:
    #     context = {'past_posts': past_posts}
    return render(request, "home/history.html", context)

@login_required(login_url='login')
def go_favorite(request):
    user = request.user
    favorites = History.objects.filter(user_id=user.id, is_favorite=True)
    favorite_posts = get_posts_by_historys(favorites)
    if favorite_posts == []:
        context = {'favorite_posts': None}
    else:
        context = {'favorite_posts': favorite_posts}
    return render(request, "home/favorite.html", context)

def get_posts_by_historys(historys):
    ids = historys.values_list('post_id', flat=True)
    return list(Post.objects.filter(id__in=ids))


@login_required(login_url='login')
def go_settings(request):
    return render(request, "home/settings.html")