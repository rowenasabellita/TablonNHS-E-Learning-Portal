from django.urls import path
from . import views
from django.conf.urls import url
# import .views


urlpatterns = [
    path('', views.login, name='login'),
    path('teacher', views.teacher, name='teacher'),
    path('teachersubject', views.teachersubject, name='teachersubject'),
    path('student', views.student, name='student'),
    path('studentsubject/<gradelevel>',
         views.studentsubject, name="studentsubject"),
    path('logout', views.logout, name='logout'),

    path('artmodule', views.artmodule, name='artmodule'),
    path('englishmodule', views.englishmodule, name='englishmodule'),
    path('espmodule', views.espmodule, name='espmodule'),
    path('filipinomodule', views.filipinomodule, name='filipinomodule'),
    path('historymodule', views.historymodule, name='historymodule'),
    path('mathmodule', views.mathmodule, name='mathmodule'),
    path('pemodule', views.pemodule, name='pemodule'),
    path('sciencemodule', views.sciencemodule, name='sciencemodule'),

    path('teacher/sm/<grade>', views.view_yearlevel, name='view_yearlevel'),
    path('yearlevel/edit', views.edit_student, name='edit_student'),

    path('teacher/um/<grade>', views.reading_material_upload,
         name='teacher/um/grade'),


    path('add_module/<gradelevel>', views.add_module,
         name='add_module'),


    path('teacher/get_quarterly_grade/<gradelevel>/<subject_id>', views.get_quarterly_grade,
         name='gradelevel'),


    path('submission/quarter/<quarter>',
         views.view_submission, name='view_submission'),
    path('get_sections', views.get_sections, name='get_sections'),
    path('get_student_records/<quarter>', views.filter_student_records,
         name='filter_student_records'),
    path('update_student_record/<id>', views.update_update_student_record,
         name='update_student_record'),


    # student
    path('get_student_analytics/<id>/<gradelevel>', views.get_student_analytics,
         name='get_student_analytics'),


    # errors
    path("error500/<redirect_to>", views.internal_server_error, name="error500")


]
