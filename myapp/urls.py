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

    path('teacher/sm/grade7', views.view_grade7, name='view_grade7'),
    path('teacher/sm/grade8', views.view_grade8, name='view_grade8'),
    path('teacher/sm/grade9', views.view_grade9, name='view_grade9'),
    path('teacher/sm/grade10', views.view_grade10, name='view_grade10'),

    path('grade7/edit/<id>', views.edit_grade7, name='edit_grade7'),
    path('grade8/edit', views.edit_grade8, name='edit_grade8'),
    path('grade9/edit', views.edit_grade9, name='edit_grade9'),
    path('grade10/edit', views.edit_grade10, name='edit_grade10'),

    path('teacher/um/grade7', views.upload_module_grade7, name='view_grade7'),
    path('teacher/um/grade8', views.upload_module_grade8, name='view_grade8'),
    path('teacher/um/grade9', views.upload_module_grade9, name='view_grade9'),
    path('teacher/um/grade10', views.upload_module_grade10, name='view_grade10'),

    path('search/', views.studentSearchInfo, name='studentSearchInfo'),



]
