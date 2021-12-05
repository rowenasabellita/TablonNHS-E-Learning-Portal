# from typing_extensions import Required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext

import myapp
from .models import UserProfile
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm
from django.contrib.auth import get_user_model

User = get_user_model()
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
def view_yearlevel(request, grade, commit=True):
    yearlevel = "Grade {}".format(grade[-1])

    students = User.objects.raw("""
                                SELECT 
                                a.id as id, a.username, a.first_name, a.last_name, b.section, b.gender, b.age, b.id as userprofile_id, b.gradelevel
                                FROM myapp_user as a 
                                JOIN myapp_userprofile as b
                                on a.id = b.user_id
                                where b.gradelevel = '{}'
                                """.format(yearlevel))

    students_data = {
        "data": []
    }
    for i in students:
        i.__dict__.update({
            "full_name": i.first_name+" "+i.last_name
        })
        students_data['data'].append(i.__dict__)

    return render(request, 'gradelevel.html', students_data)


def get_student(id):
    query = """
                SELECT 
                a.id as id, a.username, a.first_name, a.last_name, b.section, b.gender, b.age, b.id as userprofile_id, b.gradelevel
                FROM myapp_user as a 
                JOIN myapp_userprofile as b
                on a.id = b.user_id where a.id = %s
                """
    student = User.objects.raw(query, id)
    print(student)
    return student


@login_required
def edit_student(request):
    if request.method == "POST":
        req = request.POST
        user = User.objects.get(id=req['id'])
        user_profile = UserProfile.objects.get(id=req['userprofile_id'])

        user.username = req['username']
        user.first_name = req['first_name']
        user.last_name = req['last_name']
        user.save()

        user_profile.gender = req['gender']
        user_profile.age = req['age']
        user_profile.section = req['section']
        user_profile.save()

    return HttpResponse("Successfully edited student {}".format(req['username']))


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
