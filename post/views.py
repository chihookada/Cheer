from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
# from .forms import PostForm, FavoriteForm
import random
from django.core.cache import cache
cache.clear()

msg_id = -1

@login_required(login_url='login')
def go_todays_msg(request):
    messages = list(Post.objects.all())

    if messages == []:
        single_msg = {'content': "データなし", 'reference': None}
    else:
        single_msg = random.choice(messages) #choose 1 randomly
        global msg_id
        msg_id = single_msg.pk
    return render(request, "post/todays-msg.html",  {'single_msg': single_msg})

@login_required(login_url='login')
def create_new_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("completed")

    context = {"form": form}
    return render(request, "post/new-post.html", context)

@login_required(login_url='login')
def upvote(request):
    if request.method == "POST":
        if msg_id != -1:
            post = Post.objects.get(id=msg_id)
            post.likes += 1
            post.save()
            return JsonResponse({}, status=200)  # Successful upvote with empty response
    else:
        return JsonResponse({}, status=400)  # Bad request with empty response
    
@login_required(login_url='login')
# def favorite(request):
#     form = FavoriteForm()
#     if request.method == "POST":
#         form = FavoriteForm(request.POST)
#         if msg_id != -1 and form.is_valid():
#                 form.save()
#                 return JsonResponse({}, status=200)
#     else:
#         return JsonResponse({}, status=400)

@login_required(login_url='login')
def completed(request):
    return render(request, "post/completed.html")