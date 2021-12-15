from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from myapp.models.subject_model import Subject
from myapp.models.user_profile_model import UserProfile


QUARTERS = (
    (None, 'Quarters'),
    ('1st Quarter', '1st Quarter',),
    ('2nd Quarter', '2nd Quarter',),
    ('3rd Quarter', '3rd Quarter',),
    ('4th Quarter', '4th Quarter',),
)


class ClassRecord(models.Model):
    user_profile = models.ForeignKey(UserProfile,  on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,  on_delete=models.CASCADE)
    quarter = models.CharField(
        max_length=50, choices=QUARTERS, verbose_name="quarters")
    written_work = models.FloatField()
    performance_task = models.FloatField()
    quarterly_assessment = models.FloatField()
    weighted_score = models.FloatField()
    grade = models.FloatField()

    def get_all_quarters(self):
        quarters = []

        for i in QUARTERS:
            if not i[0]:
                quarters.append(i[0])
        return quarters
