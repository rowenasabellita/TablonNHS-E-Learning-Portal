# Generated by Django 3.2.7 on 2021-12-14 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_auto_20211214_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='grade_type',
            field=models.CharField(default='', max_length=45),
        ),
        migrations.AlterField(
            model_name='module',
            name='total_item',
            field=models.CharField(default=0.0, max_length=5),
        ),
    ]
