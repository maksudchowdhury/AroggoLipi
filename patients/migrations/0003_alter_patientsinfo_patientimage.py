# Generated by Django 3.2.9 on 2021-12-10 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_auto_20211205_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsinfo',
            name='patientImage',
            field=models.ImageField(upload_to='E:\\AroggoLipi Remod\\AroggoLipi Remodeled\\aroggo_lipi\\static/patientsUploadedImage'),
        ),
    ]
