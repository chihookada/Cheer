from django.db import models
from django.contrib.auth.models import AbstractUser

# # Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    reported = models.IntegerField(default=0)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []