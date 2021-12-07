from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings

from myapp.models.user_profile_model import UserProfile

GRADE10 = 'Grade 10'
GRADE9 = 'Grade 9'
GRADE8 = 'Grade 8'
GRADE7 = 'Grade 7'

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

GRADELEVEL = (
    (None, 'Grade Level'),
    (GRADE7, GRADE7),
    (GRADE8, GRADE8),
    (GRADE9, GRADE9),
    (GRADE10, GRADE10),
)


class ClassSubjects(models.Model):
    grade_level = models.CharField(
        max_length=50, choices=GRADELEVEL, verbose_name="Grade Level", blank=True)
    subjects = models.CharField(
        max_length=50, choices=SUBJECTS, verbose_name="subjects")

    def __str__(self):
        self.gradelevel_teacher = self.user_profile.gradelevel + \
            " " + self.user.first_name + " " + self.user.last_name
        return self.gradelevel_teacher


@receiver(post_save, sender=ClassSubjects)
def class_subject_signal(sender, instance, created, **kwargs):
    if created:
        ClassSubjects.objects.create(class_subject=instance)
