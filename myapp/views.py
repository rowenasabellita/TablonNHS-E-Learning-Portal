from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext

import myapp
from .models import UserProfile
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.

# myapp.User = User


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


@ login_required
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


@login_required
def view_grade7(request, commit=True):
    students = UserProfile.objects.all()
    # students = UserProfile.objects.select_related('user')
    print("select related", students)
    students_data = {
        "data": []
    }

    for i in students:
        if i.gradelevel == 'Grade 7':
            students_data['data'].append(i.__dict__)

    return render(request, 'grade7.html', students_data)


@login_required
def view_grade8(request, commit=True):
    students = UserProfile.objects.all()
    students_data = {
        "data": []
    }

    for i in students:
        if i.gradelevel == 'Grade 8':
            students_data['data'].append(i.__dict__)

    return render(request, 'grade8.html', students_data)


@login_required
def view_grade9(request, commit=True):
    students = UserProfile.objects.all()
    students_data = {
        "data": []
    }

    for i in students:
        if i.gradelevel == 'Grade 9':
            students_data['data'].append(i.__dict__)

    return render(request, 'grade9.html', students_data)


@login_required
def view_grade10(request, commit=True):
    students = UserProfile.objects.all()
    students_data = {
        "data": []
    }

    for i in students:
        if i.gradelevel == 'Grade 10':
            students_data['data'].append(i.__dict__)

    return render(request, 'grade10.html', students_data)


@login_required
def edit_grade7(request):
    return render(request, 'grade7.html')


@login_required
def edit_grade8(request):
    return render(request, 'grade8.html')


@login_required
def edit_grade9(request):
    return render(request, 'grade9.html')


@login_required
def edit_grade10(request):
    return render(request, 'grade10.html')


@login_required
def upload_module_grade7(request, commit=True):
    return render(request, 'um_grade7.html')


@login_required
def upload_module_grade8(request, commit=True):
    return render(request, 'um_grade8.html')


@login_required
def upload_module_grade9(request, commit=True):
    return render(request, 'um_grade9.html')


@login_required
def upload_module_grade10(request, commit=True):
    return render(request, 'um_grade10.html')


def teachersubject(request):
    return render(request, 'student.html')


def studentsubject(request):
    return render(request, 'studentsubject.html')


def validation(request):
    return render(request, 'validation.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def artmodule(request):
    return render(request, 'artmodule.html')


def englishmodule(request):
    return render(request, 'englishmodule.html')


def espmodule(request):
    return render(request, 'espmodule.html')


def filipinomodule(request):
    return render(request, 'filipinomodule.html')


def historymodule(request):
    return render(request, 'historymodule.html')


def mathmodule(request):
    return render(request, 'mathmodule.html')


def pemodule(request):
    return render(request, 'pemodule.html')


def sciencemodule(request):
    return render(request, 'sciencemodule.html')
