from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

from myapp.models.model1 import UserProfile
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['age', 'gender', 'address']


# class UserUpdateForm(forms.ModelForm):
#     model = User
#     fields = ['email']
