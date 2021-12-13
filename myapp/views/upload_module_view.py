from django.dispatch.dispatcher import receiver
from django.core import serializers
from django.http.response import HttpResponseServerError
from django.shortcuts import redirect, render, reverse
from django.http import HttpResponse
from django.contrib import messages
from django.utils.html import html_safe
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.class_record_model import ClassRecord
from myapp.models.module_model import Module
from myapp.models.reading_materials_model import ReadingMaterials
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
def get_quarterly_grade(request, gradelevel, subject_id):
    data = get_quarterly(gradelevel, subject_id)
    return HttpResponse(json.dumps(data))


def get_quarterly(gradelevel, subject_id):
    data = {"data": []}
    format_gradelevel = "Grade {}".format(gradelevel.split("grade")[1])

    for i in get_grade_quarterly_per_subject(format_gradelevel, subject_id):
        i.__dict__.pop("_state")

        alert = computed_grade([float(i.quarter1), float(i.quarter2),
                                float(i.quarter3), float(i.quarter4)])

        i.__dict__.update({
            "full_name": i.first_name+" "+i.last_name,
            "quarter1": str(i.quarter1) if float(i.quarter1 >= 75) else "<div style='color: red'>{}</div>".format(str(i.quarter1)),
            "quarter2": str(i.quarter2) if float(i.quarter2 >= 75) else "<div style='color: red'>{}</div>".format(str(i.quarter2)),
            "quarter3": str(i.quarter3) if float(i.quarter3 >= 75) else "<div style='color: red'>{}</div>".format(str(i.quarter3)),
            "quarter4": str(i.quarter4) if float(i.quarter4 >= 75) else "<div style='color: red'>{}</div>".format(str(i.quarter4)),
            "alert": alert[0],
            "percent": alert[1]
        })
        data['data'].append(i.__dict__)

    return data


def computed_grade(grades):
    # analytics
    alert = "<div style='color: red'>At Risk</div>"
    passing = 75

    length = 0
    percent = 0
    for i in grades:
        if i != 0:
            percent += 25
            length += 1

    grade = sum(grades) / length
    if grade >= passing:
        alert = "<div style='color: green'>No Risk</div>"

    return [alert, percent]


def get_grade_quarterly_per_subject(gradelevel, subject=None, user_id=None):
    condition = ""

    condition1 = ""
    if subject:
        condition1 = "and a.subject_id = '{}' ".format(subject)

    condition2 = ""
    if user_id:
        condition1 = "and b.user_id = '{}' ".format(user_id)

    condition = condition1+condition2

    query = """
        select 
        a.id,
        d.subject_name,
        b.gradelevel,
        c.first_name, 
        c.last_name,
        sum(case when a.quarter = '1st Quarter' then a.grade else 0 end) as quarter1,
        sum(case when a.quarter = '2nd Quarter' then a.grade else 0 end) as quarter2,
        sum(case when a.quarter = '3rd Quarter' then a.grade else 0 end) as quarter3,
        sum(case when a.quarter = '4th Quarter' then a.grade else 0 end) as quarter4

        FROM myapp_classrecord as a 
        join myapp_userprofile as b
        join myapp_user as c
        join myapp_subject as d
    
        on a.user_profile_id = b.id and b.user_id = c.id and d.id = a.subject_id
        
        where b.gradelevel = '{}' """.format(gradelevel) + condition+"""
        group by a.subject_id, b.gradelevel ,a.user_profile_id"""

    records = ClassRecord.objects.raw(query)
    return records


@login_required
def view_per_module(request, grade, subject):
    subject = Subject.objects.get(id=subject)
    record = get_quarterly(grade, subject)
    print(grade)
    return render(request, 'um_pergradelevel.html', {
        "grade": grade,
        "subject": subject.subject_name,
        "sub_id": subject.id,
        "record": record,
        "gradelevel": grade
    })


def get_module_per_subject_and_grade(request, grade, subject):
    format_gradelevel = "Grade {}".format(grade.split("grade")[1])
    module = Module.objects.filter(
        gradelevel=format_gradelevel, subject_id=subject)
    data = {"data": []}
    for i in module:
        data['data'].append({
            "id": i.id,
            "type": i.category.title(),
            "file": "<a type='button' class='btn btn-sm btn-primary' href='{}' title='{}'>Download</a>".format(i.file.name, i.file.name),
            "instruction": i.instruction,
            "created_on": str(i.created_at)
        })
    print(data)
    return HttpResponse(json.dumps(data))


@login_required
def reading_material_upload(request, grade):
    gradelevel = request.build_absolute_uri().split("/um/")[1]
    return render(request, 'um_gradelevel.html', {"subjects": get_subjects(), "cur_url": gradelevel})


@login_required
def upload_rm(request, grade):
    if request.method == 'POST':
        format_gradelevel = "Grade {}".format(grade.split("grade")[1])
        req = request.POST
        print(req.__dict__)
        try:

            rm = ReadingMaterials()
            rm.subject_id = req['subject_id']
            rm.file = request.FILES.get("document")
            rm.prepared_by_id = req['prepared_by']
            rm.gradelevel = format_gradelevel
            rm.save()
            return redirect("view_per_module", grade, req['subject_id'])

        except Exception as e:
            return render(request, 'internal_server_error.html', {"redirect_to": "/teacher", "error_msg": str(e)})


@login_required
def add_module(request, gradelevel):
    format_gradelevel = "Grade {}".format(gradelevel.split("grade")[1])

    if request.method == 'POST':
        req = request.POST
        try:
            rm = Module()
            rm.category = req['category']
            rm.date = req['date']
            rm.prepared_by_id = req['prepared_by']
            rm.instruction = req['instruction']
            rm.subject_id = req['subject_id']
            rm.gradelevel = format_gradelevel
            rm.file = request.FILES.get("document")
            rm.save()
            return redirect("view_per_module", gradelevel, req['subject_id'])
        except Exception as e:
            return render(request, 'internal_server_error.html', {"redirect_to": "/teacher", "error_msg": str(e)})
