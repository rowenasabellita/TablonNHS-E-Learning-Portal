from django.urls import path
from . import  views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('login', views.login, name = 'login'),
    path('teacher', views.teacher, name = 'teacher'),
    path('teachersubject', views.teachersubject, name = 'teachersubject'),
<<<<<<< HEAD
] 
=======
    path('student', views.student, name = 'student'),
    path('studentsubject', views.studentsubject, name = "studentsubject"),
    path('logout', views.logout, name = 'logout'),
]
>>>>>>> 583bf4e4209b861d6891af3cd5d9acd7e4c79e4c
