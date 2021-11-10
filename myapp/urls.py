from django.urls import path
from . import  views

urlpatterns = [
    path('', views.login, name = 'login'),
    # path('login', views.login, name = 'login'),
    path('teacher', views.teacher, name = 'teacher'),
    path('teachersubject', views.teachersubject, name = 'teachersubject'),
    path('student', views.student, name = 'student'),
]