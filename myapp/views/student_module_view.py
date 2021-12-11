from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.html import html_safe
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.class_record_model import ClassRecord
from myapp.models.module_model import Module
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
from myapp.views.upload_module_view import get_student_records, get_subjects, get_grade_quarterly_per_subject, get_quarterly_grade

User = get_user_model()


def teachersubject(request):
    return render(request, 'student.html')


def studentsubject(request, gradelevel):
    subjects = get_subjects()
    format_gradelevel = "Grade {}".format(gradelevel.split("grade")[1])
    module = Module.objects.filter(gradelevel=format_gradelevel)

    return render(request, 'studentsubject.html', {
        "subjects": subjects,
        "module": module,
    })


@ login_required
def get_student_analytics(request, id, gradelevel):
    format_gradelevel = "Grade {}".format(gradelevel.split("grade")[1])
    student_records = get_average_quarter(
        gradelevel=format_gradelevel, user_id=id)

    data = {
        "Written Work": [],
        "Performance Task": [],
        "Quarterly Assessment": []
    }

    for i in student_records:
        data['Written Work'].append(
            [i.written_work_quarter1 / 8,
             i.written_work_quarter2 / 8,
             i.written_work_quarter3 / 8,
             i.written_work_quarter4 / 8]
        )

        data['Performance Task'].append(
            [i.performance_task_quarter1 / 8,
             i.performance_task_quarter2 / 8,
             i.performance_task_quarter3 / 8,
             i.performance_task_quarter4 / 8]
        )

        data['Quarterly Assessment'].append(
            [i.quarterly_assessment_quarter1 / 8,
             i.quarterly_assessment_quarter2 / 8,
             i.quarterly_assessment_quarter3 / 8,
             i.quarterly_assessment_quarter4 / 8]
        )

    return HttpResponse(json.dumps(data))


def get_average_quarter(gradelevel, user_id):
    query = """select
        a.id,
        d.subject_name,
        b.gradelevel,
        c.first_name,
        c.last_name,
        sum(case when a.quarter = '1st Quarter' then a.written_work else 0 end) as written_work_quarter1,
        sum(case when a.quarter = '2nd Quarter' then a.written_work else 0 end) as written_work_quarter2,
        sum(case when a.quarter = '3rd Quarter' then a.written_work else 0 end) as written_work_quarter3,
        sum(case when a.quarter = '4th Quarter' then a.written_work else 0 end) as written_work_quarter4,

		sum(case when a.quarter = '1st Quarter' then a.quarterly_assessment else 0 end) as quarterly_assessment_quarter1,
        sum(case when a.quarter = '2nd Quarter' then a.quarterly_assessment else 0 end) as quarterly_assessment_quarter2,
        sum(case when a.quarter = '3rd Quarter' then a.quarterly_assessment else 0 end) as quarterly_assessment_quarter3,
        sum(case when a.quarter = '4th Quarter' then a.quarterly_assessment else 0 end) as quarterly_assessment_quarter4,
        
        sum(case when a.quarter = '1st Quarter' then a.performance_task else 0 end) as performance_task_quarter1,
        sum(case when a.quarter = '2nd Quarter' then a.performance_task else 0 end) as performance_task_quarter2,
        sum(case when a.quarter = '3rd Quarter' then a.performance_task else 0 end) as performance_task_quarter3,
        sum(case when a.quarter = '4th Quarter' then a.performance_task else 0 end) as performance_task_quarter4

        FROM myapp_classrecord as a
        join myapp_userprofile as b
        join myapp_user as c
        join myapp_subject as d

        on a.user_profile_id = b.id and b.user_id = c.id and d.id = a.subject_id

        where b.gradelevel = '{}' and b.user_id = '{}'
        """.format(gradelevel, user_id)

    records = ClassRecord.objects.raw(query)
    return records




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
