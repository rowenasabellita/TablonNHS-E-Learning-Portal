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


class Subject(models.Model):
    subject_name = models.CharField(
        max_length=50, choices=SUBJECTS, verbose_name="subjects")
