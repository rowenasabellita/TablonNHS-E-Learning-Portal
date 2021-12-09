from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.html import html_safe
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.class_record_model import ClassRecord
from myapp.models.subject_model import SUBJECTS, Subject
from myapp.models import UserProfile
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from myapp.forms import ProfileUpdateForm, UserUpdateForm, UploadFileForm, RecordForm
from django.contrib.auth import get_user_model
from myapp.models.class_record_model import ClassRecord
from myapp.filters import RecordFilter
from django.core.files.storage import FileSystemStorage

import json

User = get_user_model()


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_teacher:
                auth.login(request, user)
                return redirect("teacher")
            elif user.is_student:
                auth.login(request, user)
                return redirect("student")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, 'login.html')


@login_required
def teacher(request, commit=True):
    t_form = ProfileUpdateForm(instance=request.user.userprofile)

    if request.method == "POST":
        t_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if t_form.is_valid():
            t_form.save()
            messages.info(request, 'Your account has been updated!')
            return redirect("teacher")
    return render(request, 'teacher.html', {'t_form': t_form})


@login_required
def student(request, commit=True):
    s_form = ProfileUpdateForm(instance=request.user.userprofile)

    if request.method == "POST":
        s_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        if s_form.is_valid():
            s_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect("student")
    return render(request, 'student.html', {'s_form': s_form, })
