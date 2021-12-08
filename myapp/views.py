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
from .models import UserProfile
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm, UploadFileForm, RecordForm
from django.contrib.auth import get_user_model
from .models.class_record_model import ClassRecord
from .filters import RecordFilter
from django.core.files.storage import FileSystemStorage

import json

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
    return render(request, 'student.html', {'s_form': s_form, })


# sample
def student_new(request):
    return render(request, 'student_new.html')


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
def get_sections(request):
    user_profile = UserProfile()

    sections = user_profile.get_all_sections()
    return HttpResponse(json.dumps(sections))


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
