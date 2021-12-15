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
            # elif user.is_superuser:
            #     auth.login(request, user)
            #     return redirect("teacher")
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

    grade = request.user.userprofile.gradelevel.lower().replace(" ", "")
    status = get_student_status(request.user.id, grade)
    return render(request, 'student.html', {'s_form': s_form, "status": status})


def get_student_status(user_id, gradelevel):
    try:
        format_gradelevel = "Grade {}".format(gradelevel.split("grade")[1])

        average = get_average(format_gradelevel, user_id=user_id)

        completion = 0
        counter = 0
        ave = 0
        for i in average:

            if i.quarter1 != 0:
                completion += 25
                counter += 1
                ave += i.quarter1 / 8

            if i.quarter2 != 0:
                completion += 25
                counter += 1
                ave += i.quarter2 / 8

            if i.quarter3 != 0:
                completion += 25
                counter += 1
                ave += i.quarter3 / 8

            if i.quarter4 != 0:
                completion += 25
                counter += 1
                ave += i.quarter4 / 8

        final_average = ave / counter
        status = "No Risk"
        if final_average < 75:
            status = "At Risk"

        return {
            "status": status,
            "completion": completion
        }
    except:
        return {
            "status": "At Risk",
            "completion": 0
        }


def get_average(gradelevel, user_id):
    query = """
        select a.id, d.subject_name, b.gradelevel, c.first_name, c.last_name, b.user_id,
        sum(case when a.quarter = '1st Quarter' then a.grade else 0 end) as quarter1, 
        sum(case when a.quarter = '2nd Quarter' then a.grade else 0 end) as quarter2, 
        sum(case when a.quarter = '3rd Quarter' then a.grade else 0 end) as quarter3, 
        sum(case when a.quarter = '4th Quarter' then a.grade else 0 end) as quarter4 
        FROM myapp_classrecord as a 
        join myapp_userprofile as b 
        join myapp_user as c 
        join myapp_subject as d 
        on a.user_profile_id = b.id and b.user_id = c.id and d.id = a.subject_id where b.gradelevel = '{}' and b.user_id = '{}'
    """.format(gradelevel, user_id)
    print(query)
    records = ClassRecord.objects.raw(query)
    return records
