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


def get_subjects():
    subjects = Subject.objects.all()
    data = {"subjects": []}
    for s in subjects:
        data['subjects'].append(
            {"subject_name": s.subject_name, "subject_id": s.id})
    return data


def get_student_records(quarter, gradelevel=None, section=None, subject=None):
    condition1 = ""
    if gradelevel:
        condition1 = " and d.gradelevel = '{}' ".format(gradelevel)

    condition2 = ""
    if section:
        condition2 = " and d.section = '{}' ".format(section)

    condition3 = ""
    if subject:
        condition3 = " and a.subject_id = '{}' ".format(subject)

    condition = condition1 + condition2 + condition3

    query = """
        select 
        a.*, b.subject_name, c.first_name, c.last_name, d.section, d.gender, d.gradelevel, c.username
        from myapp_classrecord as a 
        join myapp_subject as b 
        join myapp_user as c 
        join myapp_userprofile d 
        on a.subject_id = b.id and a.user_profile_id = d.id and d.user_id = c.id
        where quarter = '{}' """.format(quarter) + condition+"""
        """

    records = User.objects.raw(query)
    return records
# @login_required
# def view_upload_module(request, commit=True):
#     if request.method == 'POST':
#         req = request.POST

#         myurl = req["myurl"]
#         mydate = req["mydate"]
#         mycomment = req["mycomment"]

#         activity = Activity(url=myurl, date=mydate, instruction=mycomment)
#         activity.save()
    # return render(request, 'um_gradelevel.html')


@login_required
def reading_material_upload(request, grade):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('um_gradelevel.html')
    else:
        form = UploadFileForm()

    print(get_subjects(), "sadhsa")
    return render(request, 'um_gradelevel.html', {'form': form, "subjects": get_subjects()})
