# Generated by Django 3.2.9 on 2022-01-08 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0008_diagnostictest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsinfo',
            name='patientDOB',
            field=models.DateField(),
        ),
    ]
