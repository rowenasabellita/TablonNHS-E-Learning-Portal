from django.contrib import admin
from django.forms.models import inlineformset_factory
from .models.model1 import User, StudentProfile
from .forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin

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


class ProfileInLine(admin.StackedInline):
    model = StudentProfile
    can_delete = False


class UserAdmin(UserAdmin):
    inlines = [ProfileInLine]


admin.site.register(User, UserAdmin)
