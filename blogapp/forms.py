from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Category, Comment, Post


# Form for user registration.
class RegisterForm(forms.ModelForm):
    # Meta class for RegisterForm.
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "email", "password"]


# Form for user login.
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# Form for creating or editing a blog post.
class PostForm(forms.ModelForm):
    # Meta class for PostForm.
    class Meta:
        model = Post
        fields = ["title", "content", "category", "image"]


# Form for creating a comment on a post.
class CommentForm(forms.ModelForm):
    # Meta class for CommentForm.
    class Meta:
        model = Comment
        fields = ["content"]
