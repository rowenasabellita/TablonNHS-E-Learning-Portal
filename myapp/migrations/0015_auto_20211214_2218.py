# Generated by Django 3.2.7 on 2021-12-14 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_alter_module_grade_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='performance_task',
            field=models.CharField(default=40, max_length=5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subject',
            name='quarterly_assessmend',
            field=models.CharField(default=20, max_length=5),
        ),
        migrations.AddField(
            model_name='subject',
            name='written_works',
            field=models.CharField(default=40, max_length=5),
            preserve_default=False,
        ),
    ]
