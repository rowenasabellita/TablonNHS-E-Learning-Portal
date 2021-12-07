# from typing_extensions import Required
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.utils.translation import ugettext
from django.shortcuts import render
import myapp
from myapp.models.activity_model import Activity
from myapp.models.class_subjects_model import ClassSubjects
from .models import UserProfile
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, UserUpdateForm, UploadFileForm, RecordForm
from django.contrib.auth import get_user_model
from .models.class_subjects_model import ClassSubjects
from .filters import RecordFilter

from django.core.files.storage import FileSystemStorage
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

# need subject filter (IMPORTANT!!!)
@login_required
def view_submission(request):
    records = UserProfile.objects.all()

    filters = RecordFilter(request.GET, queryset=records)
    context = {'filters': filters}

    return render(request, 'quarter.html', context)



# def view_records(request, commit-True):
#      records = User.objects.raw("""
#                                 SELECT
#                                 a.id as id, a.username, a.first_name, a.last_name, b.section, b.gradelevel b.id as userprofile_id, b.gradelevel
#                                 FROM myapp_user as a
#                                 JOIN myapp_userprofile as b
#                                 on a.id = b.user_id
#                                 where b.gradelevel = '{}'
#                                 """.format(records))
#     records_data = {
#         "data": []
#     }
#     for i in records:
#         i.__dict__.update({
#             "full_name": i.first_name+" "+i.last_name
#         })
#         records_data['data'].append(i.__dict__)

#     return render(request, 'submission.html', records_data)


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


@login_required
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


@login_required
def view_upload_module(request, commit=True):
    if request.method == 'POST':
        req = request.POST

        myurl = req["myurl"]
        mydate = req["mydate"]
        mycomment = req["mycomment"]

        activity = Activity(url=myurl, date=mydate, instruction=mycomment)
        activity.save()
    # return render(request, 'um_gradelevel.html')


@login_required
def reading_material_upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('um_gradelevel.html')
    else:
        form = UploadFileForm()

    return render(request, 'um_gradelevel.html', {'form': form})


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
