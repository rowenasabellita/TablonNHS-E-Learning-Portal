# Generated by Django 3.2.7 on 2021-12-12 14:19

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_delete_studentanalytics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='module',
            name='url',
        ),
        migrations.AddField(
            model_name='module',
            name='created_at',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='module',
            name='file',
            field=models.FileField(default='', upload_to='materials/pdf'),
        ),
        migrations.AddField(
            model_name='module',
            name='prepared_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='StudentSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('score', models.FloatField()),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.module')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile')),
            ],
        ),
    ]
