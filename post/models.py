from datetime import timezone
from django.db import models
from login.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
class Post(models.Model):
    # when a user is deleted, what I want to do with their posts
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True) # User cannot be deleted when they have at least one post
    content = models.TextField(max_length=200)
    reference = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    reports = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    active = models.BooleanField(default=True) # is open for new selection
    referenceActive = models.BooleanField(default=True)
    contentChecked = models.BooleanField(default=True) 
    referenceChecked = models.BooleanField(default=True)

    def __str__(self):
        return self.content[0:50]

class Evaluation(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, null=True) # when the post is deleted, delete the Evaluation
    is_content = models.BooleanField(default=True)
    sentiment = models.DecimalField(max_digits=10, decimal_places=9, default=10)
    toxic = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    derogatory = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    violent = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    sexual = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    insult = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    profanity = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    death_harm = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    firearms = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    public_safety = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    religion = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    illicit_drugs = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    war_conflict = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    politics = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    finance = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    legal = models.DecimalField(max_digits=10, decimal_places=9, default=-1)
    prompt = models.TextField(default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if(self.is_content):
            return self.post_id.content[0:50]
        else:
            return self.post_id.reference[0:50]
    
class History(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # when the user is deleted, delete user_fav too
    post_id = models.ForeignKey(Post, on_delete=models.PROTECT) # when the post is deleted, do not delete the user_fav
    created_at = models.DateTimeField(auto_now_add=True)
    is_seen = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_reported = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

