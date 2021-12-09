from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from myapp.models.user_profile_model import UserProfile

ALERT_STATUS = (
    (None, "Alert Status"),
    ('At Risk', 'At Risk'),
    ('No Risk', 'No Risk'),
)


class StudentAnalytics(models.Model):
    alert_status = models.CharField(
        max_length=100, choices=ALERT_STATUS, verbose_name="alert status")
    progress_percentage_quarter = models.FloatField(default=None)
    progress_percentage_school_year = models.FloatField(default=None)
