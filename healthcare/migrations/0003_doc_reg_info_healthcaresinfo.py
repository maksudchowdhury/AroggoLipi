# Generated by Django 3.2.9 on 2021-12-05 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('healthcare', '0002_delete_doctorsinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='doc_reg_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docName', models.CharField(max_length=100)),
                ('docNID', models.IntegerField()),
                ('docDOB', models.DateField()),
                ('docHospital', models.CharField(max_length=100)),
                ('docDepartment', models.CharField(max_length=100)),
                ('docEID', models.CharField(max_length=100)),
                ('docPhone', models.CharField(max_length=20)),
                ('docEmail', models.CharField(max_length=50)),
                ('docPassword', models.TextField()),
                ('docImage', models.ImageField(upload_to='doctorsUploadedImage')),
                ('accountStatus', models.CharField(default='pending', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='healthcaresInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('centerName', models.CharField(max_length=100, unique=True)),
                ('centerPassword', models.TextField()),
            ],
        ),
    ]
