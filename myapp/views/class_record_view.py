from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.html import html_safe
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.class_record_model import ClassRecord
<<<<<<< HEAD
from myapp.models.subject_model import SUBJECTS, Subject
from myapp.models import UserProfile
=======
from myapp.models.module_model import Module, StudentSubmission
from myapp.models.subject_model import SUBJECTS, Subject
from myapp.models import UserProfile
from myapp.models.user_profile_model import SECTION
>>>>>>> 2b77219593f91ddcf5029a3da4153595d47194a2
from myapp.views.profile_view import login
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from myapp.forms import ProfileUpdateForm, UserUpdateForm, UploadFileForm, RecordForm
from django.contrib.auth import get_user_model
from myapp.models.class_record_model import ClassRecord
from myapp.filters import RecordFilter
from django.core.files.storage import FileSystemStorage
from myapp.views.upload_module_view import get_student_records, get_subjects, get_grade_quarterly_per_subject
import json

User = get_user_model()
<<<<<<< HEAD

@login_required
def view_classrecord(request):

    return render(request, 'classrecord.html')
=======
grade_type = ['Written Works', 'Performance Task', 'Quarterly Assessment']


@login_required
# , grade=None, section=None, subject=None):
def view_classrecord(request, quarter):
    qt = "{} Quarter".format(quarter)

    subjects = Subject.objects.filter(id=1)
    sections = UserProfile().get_all_sections()
    header = get_headers(qt, 'Grade 7', subjects[0].id)

    default_record = get_summative_assessment(
        qt, sections['Grade 7'][0], 'Grade 7', subjects[0].id, None, header['written_work'][-3], header['performance_task'][-3])

    if len(default_record['students']) == 0:
        default_record = []

    return render(request, 'classrecord.html', {
        "subject_filter": Subject.objects.all(),
        "subjects": subjects,
        "sections": sections,
        "headers": header,
        "records": default_record,
        "quarter": quarter
    })


# @login_required
def filter_classrecord(request, quarter):
    if request.method == "POST":
        grade = request.POST["grade"]
        section = request.POST["section"]
        subject = request.POST["subject"]
        qt = "{} Quarter".format(quarter)

        header = get_headers(qt, grade, subject)

        default_record = get_summative_assessment(
            qt, section, grade, subject, None, header['written_work'][-3], header['performance_task'][-3])

        print(default_record)
        if len(default_record['students']) == 0:
            default_record = []

        data = {'records': default_record, 'header': header}
        return HttpResponse(json.dumps(data))


def get_headers(quarter, grade=None, subject=None):
    subjects = Subject.objects.filter(id=1)
    c1 = ""
    if grade:
        c1 = " and a.gradelevel = '{}'".format(grade)

    c2 = ""
    if subject:
        c2 = " and a.subject_id = '{}'".format(subject)

    condition = c1+c2

    query = """
        SELECT a.*, b.subject_name, b.performance_task, b.quarterly_assessment, b.written_works
        FROM myapp_module as a JOIN myapp_subject as b on a.subject_id = b.id
        WHERE a.quarter = '{}' """.format(quarter)+condition+"""
    """
    # print(query)

    modules = Module.objects.raw(query)
    written_work = []
    ww_total_item = 0

    performance_task = []
    pf_total_item = 0

    quarterly_assessment = []
    qa_total_item = 0

    for i in modules:
        if i.grade_type == "Written Work":
            written_work.append(i.total_item)
            ww_total_item += int(i.total_item)

        elif i.grade_type == "Performance Task":
            performance_task.append(i.total_item)
            pf_total_item += int(i.total_item)

        elif i.grade_type == "Quarterly Assessment":
            quarterly_assessment.append(i.total_item)
            qa_total_item += int(i.total_item)

    # blank if modules is less than 10
    if len(written_work) < 10:
        for i in range(10-len(written_work)):
            written_work.append("")

    if len(performance_task) < 10:
        for i in range(10-len(performance_task)):
            performance_task.append("")

    # total column (TOTAL)
    written_work.append(ww_total_item)
    performance_task.append(pf_total_item)
    quarterly_assessment.append(qa_total_item)

    # Percentage Score (PS)
    written_work.append(100)
    performance_task.append(100)
    quarterly_assessment.append(100)
    # Weighted Score (WS)
    written_work.append(subjects[0].written_works)
    performance_task.append(subjects[0].performance_task)
    quarterly_assessment.append(subjects[0].quarterly_assessment)

    return {
        "written_work": written_work,
        "performance_task": performance_task,
        "quarterly_assessment": quarterly_assessment,
    }


def get_summative_assessment(quarter, section, gradelevel, subject_id, student_id=None, ww_total_items=0, pf_total_items=0, qa_total_items=0):
    condition = ""
    if student_id:
        condition = " and a.submitted_by_id = '{}' ".format(student_id)

    query = """
        SELECT
        a.id,  b.category, b.grade_type, a.score as student_score, b.total_item, b.prepared_by_id,
        b.gradelevel, c.id as sub_id, c.subject_name, c.written_works, c.quarterly_assessment,
        c.performance_task, d.section, d.gradelevel

        FROM myapp_studentsubmission as a
        JOIN myapp_module as b
        JOIN myapp_subject as c
        JOIN myapp_userprofile as d

        on a.module_id = b.id and b.subject_id = c.id and a.submitted_by_id = d.id

        where b.quarter='{}' and d.section = '{}'
        and d.gradelevel = '{}' and b.subject_id ='{}' """.format(quarter, section, gradelevel, subject_id)+condition+"""
    """

    print(query)
    submissions = StudentSubmission.objects.raw(query)

    written_work = []
    performance_task = []
    quarterly_assessment = []
    students = []

    ww = []
    ww_total_score = 0

    pf = []
    pf_total_score = 0

    qa = []
    qa_total_score = 0

    for i in submissions:
        user = User.objects.filter(id=i.submitted_by_id)[0]
        students.append(user.first_name+" "+user.last_name)

        if i.grade_type == "Written Work":
            ww.append(int(i.student_score))
            ww_total_score += int(i.student_score)
        elif i.grade_type == "Performance Task":
            pf.append(int(i.student_score))
            pf_total_score += int(i.student_score)
        elif i.grade_type == "Quarterly Assessment":
            qa.append(int(i.student_score))
            qa_total_score += int(i.student_score)

    for l in range(10-len(ww)):
        ww.append("")
    for l in range(10-len(pf)):
        pf.append("")

        # total
    ww.append(ww_total_score)
    pf.append(pf_total_score)
    qa.append(qa_total_score)

    # PS
    ps_ww = (ww_total_score/ww_total_items) * \
        100 if ww_total_items != 0 else ww_total_items
    ps_pf = (pf_total_score/pf_total_items) * \
        100 if pf_total_items != 0 else pf_total_items
    ps_qa = (qa_total_score/qa_total_items) * \
        100 if qa_total_items != 0 else qa_total_items

    ww.append("%.2f" % round(ps_ww, 2))
    pf.append("%.2f" % round(ps_pf, 2))
    qa.append("%.2f" % round(ps_qa, 2))

    # WS

    subjects = Subject.objects.filter(id=subject_id)

    ws_ww = (int(subjects[0].written_works) / 100) * ps_ww
    ws_pf = (int(subjects[0].performance_task) / 100) * ps_pf
    ws_qa = (int(subjects[0].quarterly_assessment) / 100) * ps_qa

    ww.append("%.2f" % round(ws_ww, 2))
    pf.append("%.2f" % round(ws_pf, 2))
    qa.append("%.2f" % round(ws_qa, 2))

    written_work.append(ww)
    performance_task.append(pf)
    quarterly_assessment.append(qa)

    return {
        "students": list(set(students)),
        "written_work": written_work,
        "performance_task": performance_task,
        "quarterly_assessment": quarterly_assessment,
    }
>>>>>>> 2b77219593f91ddcf5029a3da4153595d47194a2
