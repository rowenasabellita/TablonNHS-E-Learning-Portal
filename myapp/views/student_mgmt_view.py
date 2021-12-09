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


@login_required
def view_yearlevel(request, grade, commit=True):
    yearlevel = "Grade {}".format(grade.split("grade")[1])

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


@ login_required
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
