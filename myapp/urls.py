from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('teacher', views.teacher, name='teacher'),
    path('teachersubject', views.teachersubject, name='teachersubject'),
    path('student', views.student, name='student'),
    path('studentsubject', views.studentsubject, name="studentsubject"),
    path('logout', views.logout, name='logout'),
<<<<<<< HEAD
    path('validation', views.validation, name="validation"),
=======
    # path('teacher/update_profile/<int:pk>/',
    #      views.update_profile, name='update_profile'),

>>>>>>> 318adfa5106014a6dd18d3f170441f4daa555382
]
