from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import fields
from myapp.models.reading_materials_model import ReadingMaterials

from myapp.models.user_profile_model import UserProfile
from .models import User
from . import models

SUBJECTS = (
    (None, 'Subjects'),
    ('Araling Panlipunan', 'Araling Panlipunan'),
    ('English', 'English'),
    ('ESP', 'ESP'),
    ('Filipino', 'Filipino'),
    ('MAPEH', 'MAPEH'),
    ('Math', 'Math'),
    ('Science', 'Science'),
    ('TLE', 'TLE'),
)


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


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = ReadingMaterials
        fields = ['file', 'date', 'subject']

    def __str__(self):
        return self.subject_name


class RecordForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['section', 'gradelevel']
