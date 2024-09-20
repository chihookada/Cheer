from django.db import models
# from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    # when a user is deleted, what I want to do with their posts
    # user_id = models.ForeignKey(User, on_delete=models.PROTECT) # User cannot be deleted when they have at least one post
    content = models.TextField(max_length=200)
    reference = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    reports = models.IntegerField(default=0)
    # active = models.BooleanField(default=True) # is open for new selection

    # def __str__(self):
    #     return self.content[0:50]

# class User_fav(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE) # when the user is deleted, delete user_fav too
#     post_id = models.ForeignKey(Post, on_delete=models.PROTECT) # when the post is deleted, do not delete the user_fav