from datetime import date
import time
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import environ

from login.models import User

from .models import Post, History, Evaluation
from .forms import PostForm, HistoryForm, EvaluationForm
import random
from decimal import Decimal
import threading

# Imports the Google Cloud client library
from google.cloud import language_v2
from google.cloud import translate_v3 as trans
import vertexai
from vertexai.generative_models import GenerativeModel

env = environ.Env()
environ.Env.read_env()

@login_required(login_url='login')
def go_todays_msg(request):
    msg_set = History.objects.filter(user_id=request.user.id, created_at__date=date.today(), is_reported=False)
    
    if msg_set.exists(): # already got a message today
        history = msg_set.first()
        todays_msg = Post.objects.get(id=history.post_id.pk)
        context = {
            "single_msg": todays_msg,
            "history": history
        }
        return render(request, "post/todays-msg.html",  context)
    
    # have't gotten a message today or reported one
    else:
        unseen_msges = get_unseen(request.user.id)

        if unseen_msges == []:
            single_msg = {'content': "データなし", 'reference': None}

        elif unseen_msges == "seen all":
            return render(request, "post/completed.html")

        else: #choose 1 message randomly
            single_msg = random.choice(unseen_msges) 
            single_msg.views += 1
            single_msg.save()
            
            # store the info to history
            form = HistoryForm({'user_id': request.user.id, 'post_id': single_msg.pk, 'is_seen': True})
            if form.is_valid():
                history = form.save(commit=False)
                history.save()
            else: return HttpResponse("エラーが発生しました。")# when the form is invalid

        return render(request, "post/todays-msg.html",  {'single_msg': single_msg, "history": history})

def get_unseen(user_id):
    """
        Returns a list of unseen messages. Returns "seen all" if all messages have been seen.
    """
    messages = list(Post.objects.all())
    if messages == []: # no message in the database
        return messages
    
    history = History.objects.filter(user_id=user_id)
    
    if len(history) == len(messages): # TODO consider deleted and innacive posts
        history = history.filter(is_seen=True)
        if history.count() == len(messages) or history.count() == 0:
            return "seen all"
        
    seen_post_ids = history.values_list('post_id', flat=True)
    unseen_messages = list(Post.objects.exclude(id__in=seen_post_ids, deleted=True, active=False))
    return unseen_messages        


@login_required(login_url='login')
def completed(request):
    return render(request, "post/completed.html")


@login_required(login_url='login')
def create_new_post(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.instance.user_id = request.user
            form.save() 
            flat_conent = form.cleaned_data['content']
            flat_reference = form.cleaned_data['reference']
            thread = threading.Thread(target=fetch_analysis, args=(
                flat_conent,
                flat_reference,
                form.instance.id
            ))
            thread.start()
            return redirect('posted')
        
        else: 
            context = {"form": form, "error_message": "error_message"}
            return render(request, "post/new-post.html", context)
    

    context = {"form": form}
    return render(request, "post/new-post.html", context)

@login_required(login_url='login')
def translate(request):
    PROJECT_ID = env('PROJECT_ID')
    assert PROJECT_ID
    PARENT = f"projects/{PROJECT_ID}"
    try:
        translation = translate_text(PARENT, request.POST.get('content'), request.POST.get('language'))
        translated_text = translation.translated_text
        return JsonResponse({"content": translated_text }, status=200)
    except Exception as e:
        print(str(e))
        return JsonResponse({"error": str(e)}, status=400)


def translate_text(PARENT: str, text: str, target_language_code: str) -> trans.Translation:
    client = trans.TranslationServiceClient()
    try:
        response = client.translate_text(
            parent=PARENT,
            contents=[text],
            target_language_code=target_language_code,
            mime_type="text/plain"
        )
        return response.translations[0]
    except trans.GoogleAPIError as e:  
        print(f"Translation API Error: {e}")  # Print the error for debugging
        return None
    

@login_required(login_url='login')
def upvote(request):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=request.POST.get('post_id'))
            hist = History.objects.get(id=request.POST.get('history'))
            
            post.likes += 1
            post.save()
            hist.is_liked = True
            hist.save()
            return JsonResponse({}, status=200)  # Successful upvote with empty response
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({}, status=400)  # Bad request with empty response
    
@login_required(login_url='login')
def favorite(request):
    if request.method == "POST":
        try:
            history = History.objects.get(id=request.POST.get('history'))
            history.is_favorite = not history.is_favorite
            history.save()
            return JsonResponse({}, status=200) # when history exists
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({}, status=400)

@login_required(login_url='login')
def report(request):
    if request.method == "POST":
        try:
            post = Post.objects.get(id=request.POST.get('post_id'))
            hist = History.objects.get(id=request.POST.get('history'))
            hist.is_reported = True
            hist.save()
            post.reports += 1
            post.save()
            check_num_report(post)
            return JsonResponse({'url': reverse('home'),})
        except Exception as e:
            print(str(e))
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseBadRequest()  # Bad request with empty response
    
def check_num_report(post):
    """
        Deactivates a post if the number of report is >50% of the total number of view when it is >10
    """
    if post.views > 10 and post.reports/post.view > 0.5:
        post.active = False
        post.save()    


@login_required(login_url='login')
def posted(request):
    return render(request, "post/posted.html")

def reset_history(request):
    History.objects.filter(user_id=request.user.id).update(is_seen=False)
    return redirect('home')

def fetch_analysis(content, reference=None, post_id=None):

    vertexai.init(project=env('PROJECT_ID'), location="asia-northeast1")
    model = GenerativeModel("gemini-1.5-flash-002")
    client = language_v2.LanguageServiceClient()

    def analyze_text(text, is_content):
        document = language_v2.types.Document(
            content=text, type_=language_v2.Document.Type.PLAIN_TEXT,
        )

        # Detects the sentiment of the text
        try:
            sentiment = client.analyze_sentiment(request={"document": document})
            moderate = client.moderate_text(request={"document": document})
        except Exception as e:
            print(e)
            raise SystemError

        if is_content:
            for i in range(0, 5):
                try:
                    gemini = model.generate_content("is "+text+ "a positive and encouraging message? yes or no")
                    break
                except Exception as e:
                    print(e)
                    time.sleep(2 ** i)
                    if i == 4:
                        raise SystemError
        else:
            for i in range(0, 5):
                try:
                    print(i)
                    gemini = model.generate_content("is "+text+ "a person or something that can be used as a reference? yes or no")
                    break
                except Exception as e:
                    print(e)
                    time.sleep(2 ** i)
                    if i == 4:
                        raise SystemError
        store_result(sentiment, moderate, gemini, is_content, post_id)

    # Analyze both content and reference
    analyze_text(content, True)
    if reference == None or reference != "":  # Only analyze reference if it's not empty
        analyze_text(reference, False)

    
def store_result(sentiment, moderate, gemini, is_content, post_id):
    data = {
        "post_id": post_id,
        "is_content": is_content,
        "sentiment": round(Decimal(sentiment.document_sentiment.score), 9),
        "prompt": gemini.text
    }

    categories = {
        'Toxic': 'toxic',
        'Insult': 'derogatory',
        'Profanity': 'violent',
        'Derogatory': 'sexual',
        'Sexual': 'insult',
        'Death, Harm & Tragedy': 'profanity',
        'Violent': 'death_harm',
        'Firearms & Weapons': 'firearms',
        'Public Safety': 'public_safety',
        'Health': 'religion',
        'Religion & Belief': 'illicit_drugs',
        'Illicit Drugs': 'war_conflict',
        'War & Conflict': 'finance',
        'Politics': 'politics',
        'Finance': 'finance',
        'Legal': 'legal',
    }

    for each in moderate.moderation_categories:
        field_name = categories.get(each.name, None)
        if field_name:
            data[field_name] = round(Decimal(each.confidence), 9)

    evaluation = EvaluationForm(data)
    post = Post.objects.get(id=post_id)
    if evaluation.is_valid():
        evaluation.save()

        if judge(evaluation.instance.id) == True and is_content:
            post.active = True
        elif judge(evaluation.instance.id) == True and not is_content:
            post.referenceActive = True
    
    else:
        print("evaluation not valid")
        if is_content:
            post.contentChecked = False
        else:
            post.referenceChecked = False
        post.active = False
    post.save()

def judge(evaluation_id):
    """
        returns whether the post/reference is appropriate or not
    """
    evaluation = Evaluation.objects.get(id=evaluation_id)

    criteria = { # two or more Falses below is inappropriate
        "sentiment": evaluation.sentiment >= 0.0,  # True if sentiment is positive
        "moderate": sum(getattr(evaluation, category) > 0.1 for category in ["toxic", "derogatory", "violent", "sexual", "insult", "profanity", "death_harm", "firearms", "public_safety", "illicit_drugs", "war_conflict"]) <= 2,  # True if no more than 2 moderate categories exceed the threshold
        "prompt": not (evaluation.prompt.startswith("No") or evaluation.prompt.startswith("No."))  # True if prompt doesn't start with "No" or "No."
    }

    false_count = sum(not value for value in criteria.values())
    return false_count < 2
