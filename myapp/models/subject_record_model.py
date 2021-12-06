from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from myapp.models.activity_model import Activity
from myapp.models.class_subjects_model import ClassSubjects
from myapp.models.exam_model import Exams
from myapp.models.quizzes_model import Quizzes

from myapp.models.user_profile_model import UserProfile


class SubjectRecord(models.Model):
    class_subjects = models.ForeignKey(ClassSubjects, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quizzes = models.ForeignKey(Quizzes, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE)
    average = models.IntegerField()


def __str__(self):
    self.subject_record = self.subjects + " Record"
    return self.subject_record
