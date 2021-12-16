from django.dispatch.dispatcher import receiver
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils import translation
from django.utils.html import html_safe
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.class_record_model import ClassRecord
from myapp.models.module_model import Module, StudentSubmission
from myapp.models.subject_model import SUBJECTS, Subject
from myapp.models import UserProfile
from myapp.models.user_profile_model import SECTION
from myapp.views.profile_view import login, student
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from myapp.forms import ProfileUpdateForm, UserUpdateForm, UploadFileForm, RecordForm
from django.contrib.auth import get_user_model
from myapp.models.class_record_model import ClassRecord
from myapp.filters import RecordFilter
from django.core.files.storage import FileSystemStorage, get_storage_class
from myapp.views.upload_module_view import get_student_records, get_subjects, get_grade_quarterly_per_subject
import json

User = get_user_model()
grade_type = ['Written Works', 'Performance Task', 'Quarterly Assessment']


@login_required
# , grade=None, section=None, subject=None):
def view_classrecord(request, quarter):
    qt = "{} Quarter".format(quarter)

    subjects = Subject.objects.filter(id=1)
    sections = UserProfile().get_all_sections()
    header = get_headers(qt, 'Grade 7', subjects[0].id)

    default_record = get_summative_assessment(
        quarter=qt,
        section=sections['Grade 7'][0],
        gradelevel='Grade 7',
        subject_id=subjects[0].id,
        student_id=None,
        ww_total_items=header['written_work'][-3],
        pf_total_items=header['performance_task'][-3],
        qa_total_items=int(header['quarterly_assessment'][-3])
    )
    # print(header)
    # print(default_record)

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
        # print(header)

        default_record = get_summative_assessment(
            quarter=qt,
            section=section,
            gradelevel=grade,
            subject_id=subject,
            student_id=None,
            ww_total_items=header['written_work'][-3],
            pf_total_items=header['performance_task'][-3],
            qa_total_items=int(header['quarterly_assessment'][-3])
        )

        subject_ws = Subject.objects.filter(id=subject)[0]
        subject_percent = {
            "written_work": subject_ws.written_works,
            "performance_task": subject_ws.performance_task,
            "quarterly_assessment": subject_ws.quarterly_assessment
        }
        data = {'records': default_record,
                'header': header, 'subject_percent': subject_percent}
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
        WHERE a.quarter = '{}' """.format(quarter)+condition+""" order by a.grade_type, a.date
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

    # Percentage Score (PS)
    written_work.append(100)
    performance_task.append(100)
    quarterly_assessment.append(100)

    # Weighted Score (WS)
    written_work.append(subjects[0].written_works)
    performance_task.append(subjects[0].performance_task)
    quarterly_assessment.append(subjects[0].quarterly_assessment)

    if len(quarterly_assessment) < 3:
        quarterly_assessment.insert(0, 0)

    return {
        "written_work": written_work,
        "performance_task": performance_task,
        "quarterly_assessment": quarterly_assessment,
    }


def get_submmited_modules(quarter, section, gradelevel, subject_id, student_id=None):
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
        and d.gradelevel = '{}' and b.subject_id ='{}' """.format(quarter, section, gradelevel, subject_id)+condition+""" order by b.grade_type, b.date
    """
    # print(query)
    rec = StudentSubmission.objects.raw(query)
    return rec


def get_summative_assessment(quarter, section, gradelevel, subject_id, student_id=None, ww_total_items=0, pf_total_items=0, qa_total_items=0):
    all_students = get_all_students(gradelevel, section)

    final_records = []
    for idx in range(len(all_students)):
        print(all_students[idx].id)
        ww = []
        ww_total_score = 0

        pf = []
        pf_total_score = 0

        qa = []
        qa_total_score = 0
        for mod in get_submmited_modules(quarter, section, gradelevel, subject_id, all_students[idx].user_profile_id):
            if mod.grade_type == "Written Work":
                ww.append(int(mod.student_score))
                ww_total_score += int(mod.student_score)

            elif mod.grade_type == "Performance Task":
                pf.append(int(mod.student_score))
                pf_total_score += int(mod.student_score)

            elif mod.grade_type == "Quarterly Assessment":
                qa.append(int(mod.student_score))
                qa_total_score += int(mod.student_score)

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

        final_records.append({
            "full_name": all_students[idx].first_name+" "+all_students[idx].last_name,
            "student_id": all_students[idx].user_profile_id,
            "written_work": ww,
            "performance_task": pf,
            "quarterly_assessment": qa,
            "initial_grade": update_classrecord_ws(quarter, all_students[idx].user_profile_id, subject_id, ws_ww, ws_pf, ws_qa)
        })

    return final_records


def update_classrecord_ws(quarter, student_id, subject, ww=0, pf=0, qa=0):
    cs = ClassRecord.objects.filter(
        quarter=quarter,
        user_profile_id=student_id,
        subject_id=subject
    )

    computed_ws = ww+pf+qa
    transmuted_grade = get_transmuted_grade(computed_ws)

    if cs:
        cs_doc = ClassRecord.objects.get(id=cs[0].id)
        cs_doc.quarter = quarter
        cs_doc.user_profile_id = student_id
        cs_doc.subject_id = subject
        cs_doc.written_work = ww
        cs_doc.performance_task = pf
        cs_doc.quarterly_assessment = qa
        cs_doc.weighted_score = computed_ws
        cs_doc.grade = transmuted_grade
    else:
        cs_doc = ClassRecord()
        cs_doc.quarter = quarter
        cs_doc.user_profile_id = student_id
        cs_doc.subject_id = subject
        cs_doc.written_work = 0
        cs_doc.performance_task = 0
        cs_doc.quarterly_assessment = 0
        cs_doc.weighted_score = 0
        cs_doc.grade = 0

    cs_doc.save()

    return transmuted_grade


def get_transmuted_grade(grade):
    transmutation_table = [
        [100, 100, 100],
        [98.4, 99.99, 99],
        [96.8, 98.39, 98],
        [95.2, 96.79, 97],
        [93.6, 95.19, 96],
        [61.6, 63.19, 76],
        [92.0, 93.59, 95],
        [90.4, 91.99, 94],
        [88.8, 90.39, 93],
        [87.2, 88.79, 92],
        [85.6, 87.19, 91],
        [84.0, 85.59, 90],
        [82.4, 83.99, 89],
        [80.8, 82.39, 88],
        [79.2, 80.79, 87],
        [77.6, 79.19, 86],
        [76.0, 77.59, 85],
        [74.4, 75.99, 84],
        [72.8, 74.39, 83],
        [71.2, 72.79, 82],
        [69.6, 71.19, 81],
        [68.0, 69.59, 80],
        [66.4, 67.99, 79],
        [64.8, 66.39, 78],
        [63.2, 64.79, 77],
        [60.0, 61.59, 75],
        [56.0, 59.99, 74],
        [52.0, 55.99, 73],
        [48.0, 51.99, 72],
        [44.0, 47.99, 71],
        [40.0, 43.99, 70],
        [36.0, 39.99, 69],
        [32.0, 35.99, 68],
        [28.0, 31.99, 67],
        [24.0, 27.99, 66],
        [20.0, 23.99, 65],
        [16.0, 19.99, 64],
        [12.0, 15.99, 63],
        [8.0, 11.99, 62],
        [4.0, 7.99, 61],
        [1, 3.99, 60],
        [0, 0, 0],
    ]

    final_grade = 0
    for i in transmutation_table:
        if i[0] <= grade and grade <= i[1]:
            final_grade = i[2]

    return final_grade


def get_all_students(gradelevel, section=None):
    condition = ""
    if section:
        condition = " and b.section = '{}' ".format(section)

    query = """
        SELECT
        a.*, b.id as user_profile_id,
        b.gradelevel, b.section

        FROM myapp_user as a 
        join  myapp_userprofile as b 

        on a.id = b.user_id
        where a.is_student=1 and b.gradelevel = '{}' """.format(gradelevel)+condition+"""
    """

    students = User.objects.raw(query)
    return students


@login_required
def sync_all_student(request, quarter):
    format_quarter = "{} Quarter".format(quarter)

    subjects = []
    for i in Subject.objects.all():
        subjects.append(i.id)

    gradelevels = ['Grade 7', 'Grade 8', 'Grade 9', 'Grade 10']

    for level in gradelevels:
        students = get_all_students(level)

        for student in students:

            for subject in subjects:
                update_classrecord_ws(
                    quarter=format_quarter,
                    student_id=student.user_profile_id,
                    subject=subject,
                )

    return HttpResponse(json.dumps({"status": "OK"}))
