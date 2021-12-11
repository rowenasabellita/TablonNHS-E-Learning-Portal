# Generated by Django 3.2.7 on 2021-12-10 16:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20211209_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='classrecord',
            name='quarterly_assessment',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='classrecord',
            name='weighted_score',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='studentanalytics',
            name='alert_status',
            field=models.CharField(choices=[(None, 'Alert Status'), ('At Risk', 'At Risk'), (
                'No Risk', 'No Risk')], max_length=100, verbose_name='alert status'),
        ),
    ]