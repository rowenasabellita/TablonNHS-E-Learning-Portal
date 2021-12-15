from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.html import html_safe
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.class_record_model import ClassRecord
from myapp.models.module_model import Module, StudentSubmission
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
        "cur_url": gradelevel
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


@login_required
def student_view_per_module(request, grade, subject):
    format_gradelevel = "Grade {}".format(grade.split("grade")[1])
    activity = Module.objects.filter(
        gradelevel=format_gradelevel, subject_id=subject, category="activity").order_by("date")
    exam = Module.objects.filter(
        gradelevel=format_gradelevel, subject_id=subject, category="exam").order_by("date")
    quiz = Module.objects.filter(
        gradelevel=format_gradelevel, subject_id=subject, category="quiz").order_by("date")
    subject = Subject.objects.filter(id=subject)[0]

    user_profile = UserProfile.objects.filter(user_id=request.user.id)[0].id

    ww_submission = []
    pf_submission = []
    qa_submission = []
    for i in activity:
        user = User.objects.filter(id=i.prepared_by_id)[0]
        i.prepared_by_name = user.first_name+" "+user.last_name
        sub = StudentSubmission.objects.filter(
            submitted_by_id=user_profile, module_id=i.id)
        if sub:
            i.activity_submission = sub
            if i.grade_type == "Written Work":
                ww_submission.append(sub[0].score)
            elif i.grade_type == "Performance Task":
                pf_submission.append(sub[0].score)
            if i.grade_type == "Quarterly Assessment":
                qa_submission.append(sub[0].score)

    for i in quiz:
        user = User.objects.filter(id=i.prepared_by_id)[0]
        i.prepared_by_name = user.first_name+" "+user.last_name
        sub = StudentSubmission.objects.filter(
            submitted_by_id=user_profile, module_id=i.id)
        if sub:
            i.activity_submission = sub
            if i.grade_type == "Written Work":
                ww_submission.append(sub[0].score)
            elif i.grade_type == "Performance Task":
                pf_submission.append(sub[0].score)
            if i.grade_type == "Quarterly Assessment":
                qa_submission.append(sub[0].score)

    for i in exam:
        user = User.objects.filter(id=i.prepared_by_id)[0]
        i.prepared_by_name = user.first_name+" "+user.last_name
        sub = StudentSubmission.objects.filter(
            submitted_by_id=user_profile, module_id=i.id)
        if sub:
            i.activity_submission = sub
            if i.grade_type == "Written Work":
                ww_submission.append(sub[0].score)
            elif i.grade_type == "Performance Task":
                pf_submission.append(sub[0].score)
            if i.grade_type == "Quarterly Assessment":
                qa_submission.append(sub[0].score)

    ww_header = get_header_basis(format_gradelevel, subject, 'Written Work')
    pf_header = get_header_basis(
        format_gradelevel, subject, 'Performance Task')
    qa_header = get_header_basis(
        format_gradelevel, subject, 'Quarterly Assessment')

    next_scores = []

    next_scores.append(get_next_score(ww_header, ww_submission))
    next_scores.append(get_next_score(pf_header, pf_submission))
    next_scores.append(get_next_score(qa_header, qa_submission))

    for n in next_scores:
        for i in activity:
            if i.id == n["next_module"]:
                i.next_score = int(n['next_score'])
                i.next_percent = n['percent']

        for i in quiz:
            if i.id == n["next_module"]:
                i.next_score = int(n['next_score'])
                i.next_percent = n['percent']

        for i in exam:
            if i.id == n["next_module"]:
                i.next_score = int(n['next_score'])
                i.next_percent = n['percent']

    data = {
        "activity": activity,
        "exam": exam,
        "quiz": quiz,
        "subject_name": subject.subject_name,
        "subject_id": subject.id,
    }
    return render(request, 'student_persubject.html', data)


def get_header_basis(grade, subject, gtype):
    module = Module.objects.filter(
        gradelevel=grade, subject_id=subject, grade_type=gtype).order_by('date')
    subject_percentage = Subject.objects.filter(id=module[0].subject_id)

    total_items = []
    modules = []
    for i in module:
        total_items.append(i.total_item)
        modules.append(i.id)

    return {
        'total_items': total_items,
        'modules': modules,
        'subject_percentage': subject_percentage[0]
    }


def get_percentage(score, total):
    return (score/total)*100


def get_next_score(head, submission):
    count = 1
    total_percentage = 0
    for i in range(len(submission)):
        count += 1
        percentage = get_percentage(
            submission[i], float(head['total_items'][i]))

        total_percentage += percentage

    x = (60*count) - total_percentage
    next_percent = abs(x)
    if len(submission) >= len(head['total_items']):
        next_score = None
        next_module = None
    else:
        next_score = (next_percent/100) * float(head['total_items'][count-1])
        next_module = head['modules'][count-1]

    return {
        "percent": next_percent,
        "next_score": next_score,
        "next_module": next_module
    }


@login_required
def submit_activity(request):
    try:
        if request.method == 'POST':
            req = request.POST
            print(req.__dict__)

            user_profile = UserProfile.objects.filter(
                user_id=request.user.id)[0].id
            submit = StudentSubmission()
            submit.file = request.FILES.get('document')
            submit.comments = req['comment']
            submit.submitted_by_id = user_profile
            submit.score = 0.00
            submit.module_id = req['module_id']
            submit.save()
            return redirect("student_view_per_module", req['grade'], req['subject_id'])
    except Exception as e:
        return render(request, 'internal_server_error.html', {"redirect_to": "/student", "error_msg": str(e)})


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
