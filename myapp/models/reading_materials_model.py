from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from myapp.models.class_subjects_model import ClassSubjects
from myapp.models.user_profile_model import UserProfile
import datetime


class ReadingMaterials(models.Model):
    file = models.FileField(
        default="", upload_to='materials/pdf', max_length=100)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        self.activity = self.date + " " + self.subjects
        return self.activity
