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
    date = models.DateField()  # due date
    instruction = models.TextField(verbose_name="Instruction", max_length=500)
    gradelevel = models.TextField(verbose_name="Gradelevel", max_length=50)
    prepared_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file = models.FileField(
        default="", upload_to='materials/pdf', max_length=100)
    created_at = models.DateField(auto_now_add=True)


class StudentSubmission(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    submitted_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    submission_date = models.DateField(auto_now_add=True)
    score = models.FloatField()
    file = models.FileField(
        default="", upload_to='materials/pdf', max_length=100)
    created_at = models.DateField(auto_now_add=True)
