# Generated by Django 3.2.7 on 2021-12-06 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20211206_2103'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='gradelevel',
            new_name='class_subject',
        ),
        migrations.RenameField(
            model_name='exams',
            old_name='gradelevel',
            new_name='class_subject',
        ),
        migrations.RenameField(
            model_name='quizzes',
            old_name='gradelevel',
            new_name='class_subject',
        ),
        migrations.RenameField(
            model_name='readingmaterials',
            old_name='gradelevel',
            new_name='class_subject',
        ),
    ]
