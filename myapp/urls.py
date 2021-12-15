from django.urls import path, re_path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
# import .views


urlpatterns = [
    path('', views.login, name='login'),
    path('teacher', views.teacher, name='teacher'),
    path('teachersubject', views.teachersubject, name='teachersubject'),
    path('student', views.student, name='student'),
    path('studentsubject/<gradelevel>',
         views.studentsubject, name="studentsubject"),

    #     path('allsubjects', views.all_subjects_view, name="allsubjects"),

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

    # upload module
    path('teacher/um/<grade>', views.reading_material_upload,
         name='reading_material_upload'),  # view
    path('teacher/um/upload/<grade>', views.upload_rm,
         name='upload_rm'),  # upload reading material
    path('add_module/<gradelevel>', views.add_module,
         name='add_module'),  # add module per type (quiz, exam, activity)
    path('view_per_module/<grade>/<subject>', views.view_per_module,
         name='view_per_module'),  # add module per type (quiz, exam, activity)

    # module per subject view
    path('teacher/get_quarterly_grade/<gradelevel>/<subject_id>', views.get_quarterly_grade,
         name='get_quarterly_grade'),
    path('teacher/get_module_per_subject_and_grade/<grade>/<subject>', views.get_module_per_subject_and_grade,
         name='get_module_per_subject_and_grade'),
    path('teacher/view_subject_record/<grade>/<subject>/<category>/<module_id>',
         views.view_subject_record, name='view_subject_record'),
    path('teacher/update_score/',
         views.udpate_score, name='update_score'),

    # class record
    path('classrecord/<quarter>',
         views.view_classrecord, name='view_classrecord'),
    path('filter_classrecord/<quarter>',
         views.filter_classrecord, name='filter_classrecord'),



    path('classrecord', views.view_classrecord, name='view_classrecord'),

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
    path("error500/<redirect_to>", views.internal_server_error, name="error500"),





    # student url
    path("student/view_per_module/<grade>/<subject>",
         views.student_view_per_module, name='student_view_per_module'),
    path("student/submit_activity",
         views.submit_activity, name='submit_activity'),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
