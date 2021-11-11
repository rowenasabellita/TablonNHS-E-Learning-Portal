from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from myproject.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User, auth

# Create your views here.

# def home(request):
#     return render(request, 'home.html')
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("teacher")
        else:
            messages.info(request, "Invalid credentials")
            return redirect("login")
    else:
        # return render(request, {"title": "Login"})
        return render(request, 'login.html')

    # return render(request, 'login.html')
def teacher(request):
    return render(request, 'teacher.html')
def teachersubject(request):
    return render(request, 'teachersubject.html')    
def student(request):
    return render(request, 'student.html')   
def studentsubject(request):
    return render(request, 'studentsubject.html')  
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')

