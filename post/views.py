from datetime import date
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Post, History 
from .forms import PostForm, HistoryForm

import random

msg_id = -1

@login_required(login_url='login')
def go_todays_msg(request):
    msg_set = History.objects.filter(user_id=request.user.id, created_at__date=date.today())
    # already got a message today
    if msg_set.exists():
        his_object = msg_set.first()
        todays_msg = Post.objects.get(id=his_object.post_id.pk)
        its_history = History.objects.get(id=his_object.pk)
        context = {
            "single_msg": todays_msg,
            "favorite": its_history.is_favorite,
            "like": its_history.is_liked
        }
        return render(request, "post/todays-msg.html",  context)
    
    # have't gotten a message today
    else:
        unseen_msges = get_unseen(request.user.id)

        if unseen_msges == []:
            single_msg = {'content': "データなし", 'reference': None}

        elif unseen_msges == "seen all":
            return render(request, "post/completed.html")

        else:
            single_msg = random.choice(unseen_msges) #choose 1 randomly
            global msg_id
            msg_id = single_msg
            
            # store the info to history
            form = HistoryForm({'user_id': request.user.id, 'post_id': msg_id})
            if form.is_valid():
                form.save()
            else: return HttpResponse("エラーが発生しました。")# when the form is invalid

        return render(request, "post/todays-msg.html",  {'single_msg': single_msg})

def get_unseen(user_id):
    messages = list(Post.objects.all())
    history = History.objects.filter(user_id=user_id)
    if messages == []: # no message in the database
        return messages
    
    elif len(history) == len(messages): # all messages have been seen
        return "seen all"
    
    seen_post_ids = history.values_list('post_id', flat=True)
    unseen_messages = list(Post.objects.exclude(id__in=seen_post_ids))
    return unseen_messages        


@login_required(login_url='login')
def completed(request):
    return render(request, "post/completed.html")


@login_required(login_url='login')
def create_new_post(request):
    form = PostForm()
    if request.method == "POST":
        print(request.user.id)
        form = PostForm(request.POST)
        print(form)
        if form.is_valid():
            form.instance.user_id = request.user
            form.save()
            
            return redirect('posted')
        
        else: 
            context = {"form": form, "error_message": "error_message"}
            return render(request, "post/new-post.html", context)
    

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
def favorite(request):
    if request.method == "POST":
        history = History.objects.get(user_id=request.POST.get('user_id'), post_id=request.POST.get('post_id'))
        if history:
            history.is_favorite = not history.is_favorite
            history.save()
            return JsonResponse({}, status=200) # when history exists
        else: return JsonResponse({}, status=400) # when history does not exist
        # if History.objects.filter(user_id=request.POST.get('user_id'), post_id=request.POST.get('post_id')).exists() is False:
        #     if form.is_valid():
        #         form.save()
        #         return JsonResponse({}, status=200) # when first time favoriting
        #     else: return JsonResponse({}, status=400) # when the form is invalid
        # else: return JsonResponse({}, status=200) # when it has been favorited
    else: 
        return JsonResponse({}, status=400) # when request.method != "POST"

@login_required(login_url='login')
def posted(request):
    return render(request, "post/posted.html")

def reset_history(request):
    return redirect('home')