# Generated by Django 3.2.7 on 2021-12-06 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20211206_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='class_subject',
            new_name='gradelevel',
        ),
        migrations.RenameField(
            model_name='classsubjects',
            old_name='gradelevel',
            new_name='user_profile',
        ),
        migrations.RenameField(
            model_name='exams',
            old_name='class_subject',
            new_name='gradelevel',
        ),
        migrations.RenameField(
            model_name='quizzes',
            old_name='class_subject',
            new_name='gradelevel',
        ),
        migrations.RenameField(
            model_name='readingmaterials',
            old_name='class_subject',
            new_name='gradelevel',
        ),
    ]
