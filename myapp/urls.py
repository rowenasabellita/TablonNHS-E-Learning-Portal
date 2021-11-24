from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('teacher', views.teacher, name='teacher'),
    path('teachersubject', views.teachersubject, name='teachersubject'),
    path('student', views.student, name='student'),
    path('studentsubject', views.studentsubject, name="studentsubject"),
    path('logout', views.logout, name='logout'),
    # path('teacher/update_profile/<int:pk>/',
    #      views.update_profile, name='update_profile'),

]
