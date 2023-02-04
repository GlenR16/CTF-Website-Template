from django.contrib.auth.forms import UserCreationForm, UserChangeForm,AuthenticationForm,PasswordChangeForm
from .models import User
from django import forms
from django.utils.safestring import mark_safe

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Full Name'}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Password Confirmation'}))

    class Meta(UserCreationForm):
        model = User
        fields = ('email','name')


# class UserChangeForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = ('email','name')

class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    class Meta:
        model = User
        fields = ('email','password')

class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Old Password'}))
    new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'New Password'}))
    new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'New Password Confirmation'}))
    class Meta:
        model = User