from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields

from myapp.models.model1 import StudentProfile
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = "__all__"


class UserUpdateForm(forms.ModelForm):
    model = User
    fields = ['email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['age', 'gender', 'address']
