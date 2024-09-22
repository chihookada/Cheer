from django.forms import ModelForm
from .models import Post, History

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'reference']

class HistoryForm(ModelForm):
    class Meta:
        model = History
        fields = ['user_id', 'post_id']