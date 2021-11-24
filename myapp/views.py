from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext
from .models import StudentProfile
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm


# Create your views here.


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
    t_form = ProfileUpdateForm(instance=request.user.studentprofile)

    if request.method == "POST":
        t_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.studentprofile)
        if t_form.is_valid():
            t_form.save()
            messages.info(request, 'Your account has been updated!')
            return redirect("teacher")
    return render(request, 'teacher.html', {'t_form': t_form})


@ login_required
def student(request, commit=True):
    s_form = ProfileUpdateForm(instance=request.user.studentprofile)

    if request.method == "POST":
        s_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.studentprofile)
        if s_form.is_valid():
            s_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect("student")
    return render(request, 'student.html', {'s_form': s_form, })


def teachersubject(request):
    return render(request, 'student.html')


def studentsubject(request):
    return render(request, 'studentsubject.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


def mathmodule(request):
    return render(request, 'mathmodule.html')
