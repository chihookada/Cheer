from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils.translation import gettext as _

from login.models import User
from post.models import History, Post

from datetime import date, timedelta

# Create your views here.
@login_required(login_url='login')
def go_home(request):
    """
        Goes to the home page after checking if a message to show exists. 
        Depending on whether it has one, it redirects to todays-msg page or runs a selection to pick a new one.
    """
    if request.user.active is False:
        logout(request)

    todays_msg = History.objects.filter(user_id=request.user.id, created_at__date=date.today())
    if todays_msg.filter(is_reported=False).exists(): # has a message to be shown
        return redirect('todays-msg') 
    elif todays_msg.exists(): # has reported a post
        return render(request, "home/home.html")
    
    # first log-in of the day, collect the number of Goods from yesterday
    good_count = review(request)
    context = {"count": good_count, "warn": assess_user(request)}
    return render(request, "home/home.html", context)

def review(request):
    """
        Collect the number of Goods received yesterday on previous posts and return it
    """
    posts_yesterday = History.objects.filter(created_at__date=date.today()-timedelta(days=1), post_id__user_id=request.user.id, is_liked = True)
    return posts_yesterday.count()

def assess_user(request):
    """
        Get the number of posts that are deactivated from innappropriate posts
        Returns None: no warning, 1: first warning, 2: last warning, 3: account deactivation
    """
    posts = Post.objects.filter(user_id=request.user.id, reports__gt=5, active=False)
    if posts.count() > 6:
        User.objects.filter(id=request.user_id).active = False
        logout(request)
        return 3
    elif posts.count() > 4:
        return 2
    elif posts.count() > 2:
        return 1
    return

def go_home_guest(request):
    return render(request, "home/home-guest.html")

@login_required(login_url='login')
def go_history(request):
    # user = request.user
    past_posts = Post.objects.filter(user_id=request.user.id, deleted=False).order_by('-created_at')
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
    """
        Helper function to return Post objects from given historys
    """
    ids = historys.values_list('post_id', flat=True)
    return list(Post.objects.filter(id__in=ids))

@login_required(login_url='login')
def go_settings(request):
    languages = [{'code': 'en', 'name_local': 'English'}, {'code': 'ja', 'name_local': '日本語'}]
    return render(request, "home/settings.html", {"languages": languages})

@login_required(login_url='login')
def delete_post(request):
    if request.method == "POST":
        post = Post.objects.get(id=request.POST.get('post_id'))
        if post:
            post.deleted = True
            post.save()
            return JsonResponse({}, status=200)
        else: return JsonResponse({}, status=400)
    else: 
        return JsonResponse({}, status=400) # when request.method != "POST"

@login_required(login_url='login')
def delete_fav(request):
    if request.method == "POST":
        history = History.objects.get(post_id=request.POST.get('post_id'), user_id=request.user.id)
        if history:
            history.is_favorite = False
            history.save()
            return JsonResponse({}, status=200)
        else: return JsonResponse({}, status=400)
    else: 
        return JsonResponse({}, status=400) # when request.method != "POST"
