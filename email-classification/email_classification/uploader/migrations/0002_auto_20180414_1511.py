# Generated by Django 2.0.3 on 2018-04-14 15:11

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploader', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='content',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='temp-email-storage'), upload_to=''),
        ),
    ]