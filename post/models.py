from django.db import models
from login.models import User

# Create your models here.
class Post(models.Model):
    # when a user is deleted, what I want to do with their posts
    user_id = models.ForeignKey(User, on_delete=models.PROTECT, null=True) # User cannot be deleted when they have at least one post
    content = models.TextField(max_length=200)
    reference = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    reports = models.IntegerField(default=0)
    active = models.BooleanField(default=True) # is open for new selection

    def __str__(self):
        return self.content[0:50]

# class Favorite(models.Model):
#     user_id = models.ForeignKey(User, on_delete=models.CASCADE) # when the user is deleted, delete user_fav too
#     post_id = models.ForeignKey(Post, on_delete=models.PROTECT) # when the post is deleted, do not delete the user_fav
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user_id', 'post_id')
#         ordering = ['-created_at']

class History(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) # when the user is deleted, delete user_fav too
    post_id = models.ForeignKey(Post, on_delete=models.PROTECT) # when the post is deleted, do not delete the user_fav
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    favorited_at = models.DateTimeField(null=True, blank=True)
    is_liked = models.BooleanField(default=False)
    liked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
