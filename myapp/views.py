from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html')
def login(request):
<<<<<<< HEAD
    return render(request, 'login.html')
=======
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
        return render(request, 'login.html')

>>>>>>> 583bf4e4209b861d6891af3cd5d9acd7e4c79e4c
def teacher(request):
    return render(request, 'teacher.html')
def teachersubject(request):
    return render(request, 'teachersubject.html')    
<<<<<<< HEAD
=======
def student(request):
    return render(request, 'student.html')   
def studentsubject(request):
    return render(request, 'studentsubject.html')  
    
def logout(request):
    auth.logout(request)
    return render(request, 'login.html')

>>>>>>> 583bf4e4209b861d6891af3cd5d9acd7e4c79e4c
