from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1']

#
# class FollowingForm(forms.ModelForm):
#     class Meta:
#         model = Follow
#         fields = '__all__'




class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'id': 'exampleFormControlInput1', 'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '10', 'id': "exampleFormControlTextarea1"}),
            # 'image': forms.ImageField(attrs={'class': 'btn-primary'})
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '5', 'id': "exampleFormControlTextarea1"})

        }
