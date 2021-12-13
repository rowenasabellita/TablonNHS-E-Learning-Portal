from django.contrib import admin
from django.forms.models import inlineformset_factory
from .models.user_profile_model import User, UserProfile
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.db import IntegrityError
from .models.class_subjects_model import ClassSubjects
from .models.activity_model import Activity
from .models.quizzes_model import Quizzes
from .models.exam_model import Exams
from .models.reading_materials_model import ReadingMaterials
from .models.subject_record_model import SubjectRecord

# Register your models here..


class UserAdmin(UserAdmin):
    model = User
    add_form = UserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'User type',
            {
                'fields': (
                    'is_student',
                    'is_teacher',
                )
            }
        )
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(ClassSubjects)
admin.site.register(Activity)
admin.site.register(Quizzes)
admin.site.register(Exams)


admin.site.register(ReadingMaterials)
admin.site.register(SubjectRecord)
