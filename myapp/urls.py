from django.urls import path
from . import  views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login', views.login, name = 'login'),
    path('teacher', views.teacher, name = 'teacher'),
    path('teachersubject', views.teachersubject, name = 'teachersubject'),
] 