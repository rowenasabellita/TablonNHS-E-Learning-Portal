from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('teacher', views.teacher, name='teacher'),
    path('teachersubject', views.teachersubject, name='teachersubject'),
    path('student', views.student, name='student'),
    path('studentsubject', views.studentsubject, name="studentsubject"),
    path('logout', views.logout, name='logout'),
    path('artmodule', views.artmodule, name='artmodule'),
    path('englishmodule', views.englishmodule, name='englishmodule'),
    path('espmodule', views.espmodule, name='espmodule'),
    path('filipinomodule', views.filipinomodule, name='filipinomodule'),
    path('historymodule', views.historymodule, name='historymodule'),
    path('mathmodule', views.mathmodule, name='mathmodule'),
    path('pemodule', views.pemodule, name='pemodule'),
    path('sciencemodule', views.sciencemodule, name='sciencemodule'),


]
