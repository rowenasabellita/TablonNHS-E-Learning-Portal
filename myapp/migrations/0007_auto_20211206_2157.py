# Generated by Django 3.2.7 on 2021-12-06 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20211206_2124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='class_subject',
        ),
        migrations.RemoveField(
            model_name='exams',
            name='class_subject',
        ),
        migrations.RemoveField(
            model_name='quizzes',
            name='class_subject',
        ),
        migrations.RemoveField(
            model_name='readingmaterials',
            name='class_subject',
        ),
    ]
