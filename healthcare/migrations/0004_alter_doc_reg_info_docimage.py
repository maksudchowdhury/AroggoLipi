# Generated by Django 3.2.9 on 2021-12-10 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('healthcare', '0003_doc_reg_info_healthcaresinfo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doc_reg_info',
            name='docImage',
            field=models.ImageField(upload_to='E:\\AroggoLipi Remod\\AroggoLipi Remodeled\\aroggo_lipi\\static/doctorsUploadedImage'),
        ),
    ]
