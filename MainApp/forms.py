from django import forms
from .models import Snippet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Comment


class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['name', 'code', 'is_hidden']
  
class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'image']
