# Generated by Django 3.2.7 on 2021-12-12 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20211212_2219'),
    ]

    operations = [
        migrations.AddField(
            model_name='readingmaterials',
            name='prepared_by',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='myapp.userprofile'),
            preserve_default=False,
        ),
    ]