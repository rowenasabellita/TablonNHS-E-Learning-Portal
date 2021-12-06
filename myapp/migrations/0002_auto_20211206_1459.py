# Generated by Django 3.2.7 on 2021-12-06 06:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('date', models.DateField()),
                ('instruction', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='ClassSubjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.CharField(choices=[(None, 'Subjects'), ('Araling Panlipunan', 'Araling Panlipunan'), ('English', 'English'), ('ESP', 'ESP'), ('Filipino', 'Filipino'), ('MAPEH', 'MAPEH'), ('Math', 'Math'), ('Science', 'Science'), ('TLE', 'TLE')], max_length=50, verbose_name='subjects')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Exams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('date', models.DateField()),
                ('instruction', models.TextField(max_length=500)),
                ('class_subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.classsubjects')),
            ],
        ),
        migrations.CreateModel(
            name='Quizzes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('date', models.DateField()),
                ('instruction', models.TextField(max_length=500)),
                ('class_subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.classsubjects')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average', models.IntegerField()),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.activity')),
                ('class_subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.classsubjects')),
                ('exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.exams')),
                ('quizzes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.quizzes')),
            ],
        ),
        migrations.CreateModel(
            name='ReadingMaterials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=500)),
                ('date', models.DateField()),
                ('class_subjects', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.classsubjects')),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='class_subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.classsubjects'),
        ),
    ]
