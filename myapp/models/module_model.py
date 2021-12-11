from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from myapp.models.subject_model import Subject
from myapp.models.user_profile_model import UserProfile

CATEGORY = (
    (None, 'Category'),
    ('Activity', 'Activity'),
    ('Quiz', 'Quiz'),
    ('Exam', 'Exam'),
)


class Module(models.Model):
    subject = models.ForeignKey(Subject,  on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50, choices=CATEGORY, verbose_name="Category")
    url = models.URLField(max_length=500)
    date = models.DateField()
    instruction = models.TextField(verbose_name="Instruction", max_length=500)
    gradelevel = models.TextField(verbose_name="Gradelevel", max_length=50)

    def __str__(self):
        self.activity = self.date + " " + self.subjects
        return self.activity
