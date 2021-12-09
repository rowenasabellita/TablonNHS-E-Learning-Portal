from django.contrib import admin
from django.forms.models import inlineformset_factory

from myapp.models.class_record_model import ClassRecord
from .models.user_profile_model import User, UserProfile
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
from django.db import IntegrityError


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
