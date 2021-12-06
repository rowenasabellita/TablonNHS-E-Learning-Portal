from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from myapp.models.user_profile_model import UserProfile

SUBJECTS = (
    (None, 'Subjects'),
    ('Araling Panlipunan', 'Araling Panlipunan'),
    ('English', 'English'),
    ('ESP', 'ESP'),
    ('Filipino', 'Filipino'),
    ('MAPEH', 'MAPEH'),
    ('Math', 'Math'),
    ('Science', 'Science'),
    ('TLE', 'TLE'),
)


class ClassSubjects(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subjects = models.CharField(
        max_length=50, choices=SUBJECTS, verbose_name="subjects")

    def __str__(self):
        self.gradelevel_teacher = self.user_profile.gradelevel + \
            " " + self.user.first_name + " " + self.user.last_name
        return self.gradelevel_teacher
