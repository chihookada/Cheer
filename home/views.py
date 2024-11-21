from datetime import date
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from post.models import History, Post


# Create your views here.
@login_required(login_url='login')
def go_home(request):
    todays_msg = History.objects.filter(user_id=request.user.id, created_at__date=date.today(), is_reported=False)
    if todays_msg.exists():
        return redirect('todays-msg')  # Redirect if history exists for today
    return render(request, "home/home.html")

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
    ids = historys.values_list('post_id', flat=True)
    return list(Post.objects.filter(id__in=ids))

@login_required(login_url='login')
def go_settings(request):
    return render(request, "home/settings.html")

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
    print("here2")
    if request.method == "POST":
        history = History.objects.get(post_id=request.POST.get('post_id'), user_id=request.user.id)
        if history:
            history.is_favorite = False
            history.save()
            return JsonResponse({}, status=200)
        else: return JsonResponse({}, status=400)
    else: 
        return JsonResponse({}, status=400) # when request.method != "POST"
