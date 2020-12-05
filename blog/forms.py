from django import forms
from .models import Blog, Photo, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)