from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    return render(request, 'home.html')
def login(request):
    return render(request, 'login.html')
def teacher(request):
    return render(request, 'teacher.html')
def teachersubject(request):
    return render(request, 'teachersubject.html')    
