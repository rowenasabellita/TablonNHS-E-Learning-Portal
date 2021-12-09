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
from myapp.views.upload_module_view import get_student_records, get_subjects
import json

User = get_user_model()


@login_required
def view_submission(request, quarter):

    records = get_student_records("{} Quarter".format(quarter))

    sections = UserProfile().get_all_sections()

    context = {
        "gradelevel": sections,
        "subjects": get_subjects,
        "records": [],
    }

    counter = 0
    for r in records:
        counter += 1
        r.__dict__.update({
            "full_name": r.first_name+" "+r.last_name,
            "counter": counter
        })
        context['records'].append(r.__dict__)

    return render(request, 'quarter.html', context)


@login_required
def filter_student_records(request, quarter):
    if request.method == "POST":
        df = request.POST
        records = get_student_records("{} Quarter".format(
            quarter), df['gradelevel'], df['section'], df['subject'])

        data = {"data": []}
        counter = 0
        for r in records:
            counter += 1
            r.__dict__.pop('_state')
            r.__dict__.update({
                "full_name": r.first_name+" "+r.last_name,
                "counter": counter
            })
            data['data'].append(r.__dict__)
        return HttpResponse(json.dumps(data))


@login_required
def update_update_student_record(request, id):
    if request.method == "POST":
        df = request.POST
        record = ClassRecord.objects.get(id=id)
        print(df['field'], df['val'])
        if df['field'] == "written_work":
            record.written_work = df['val']
        elif df['field'] == "performance_task":
            record.performance_task = df['val']
        elif df['field'] == "grade":
            record.grade = df['val']

        record.save()
        return HttpResponse(json.dumps({"status": "OK"}))


@login_required
def get_quarterly_grade(request, gradelevel):
    data = {"data": []}
    format_gradelevel = "Grade {}".format(gradelevel[-1])

    for i in get_grade_quarterly_per_subject(format_gradelevel):
        i.__dict__.pop("_state")
        i.__dict__.update({
            "full_name": i.first_name+" "+i.last_name,
            "quarter1": str(i.quarter1),
            "quarter2": str(i.quarter2),
            "quarter3": str(i.quarter3),
            "quarter4": str(i.quarter4),
        })
        data['data'].append(i.__dict__)
    return HttpResponse(json.dumps(data))


def get_grade_quarterly_per_subject(gradelevel, subject=None):
    condition = ""
    if subject:
        condition = "and subject_id = '{}' ".format(subject)

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
    print(records)
    return records


@login_required
def get_sections(request):
    user_profile = UserProfile()

    sections = user_profile.get_all_sections()
    return HttpResponse(json.dumps(sections))
