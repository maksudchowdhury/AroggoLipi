# Generated by Django 3.2.9 on 2022-01-08 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0007_auto_20220108_2329'),
    ]

    operations = [
        migrations.CreateModel(
            name='diagnosticTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientEmail', models.CharField(default=False, max_length=50)),
                ('visitingDate', models.DateField()),
                ('diagTest', models.CharField(max_length=300)),
            ],
        ),
    ]
