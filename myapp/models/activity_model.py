from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from myapp.models.class_subjects_model import ClassSubjects

from myapp.models.user_profile_model import UserProfile


class Activity(models.Model):
    class_subjects = models.ForeignKey(ClassSubjects, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)
    date = models.DateField()
    instruction = models.TextField(max_length=500)

    def __str__(self):
        self.activity = self.date + " " + self.subjects
        return self.activity
