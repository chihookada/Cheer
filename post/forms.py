from django.forms import ModelForm
from .models import Post
# from .models import Post, User_fav

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'reference']

# class FavoriteForm(ModelForm):
#     class Meta:
#         model = User_fav
#         fields = '__all__'