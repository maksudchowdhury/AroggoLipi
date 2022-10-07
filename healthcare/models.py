
# Create your models here.

# healthcare login model
# docRequest model
from django.db import models
from django.db.models.base import Model
from aroggo_lipi.settings import BASE_DIR
import os
#


class doc_reg_info(models.Model):
    docName = models.CharField(max_length=100)
    docNID = models.IntegerField()
    docDOB = models.DateField()
    docHospital = models.CharField(max_length=100)
    docDepartment = models.CharField(max_length=100)
    docEID = models.CharField(max_length=100)
    docPhone = models.CharField(max_length=20)
    docEmail = models.CharField(max_length=50)
    docPassword = models.TextField()

    docImage = models.ImageField(upload_to=os.path.join(
        BASE_DIR, 'static/doctorsUploadedImage'))
    accountStatus = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.docName


class healthcareCenter(models.Model):
    centerName = models.CharField(max_length=100, unique=True)
    centerPassword = models.TextField()

    def __str__(self):
        return self.centerName


class healthcareDepartment(models.Model):
    deptName = models.CharField(max_length=100, unique=True)
    deptDescription = models.TextField()
    deptRemarks = models.TextField()

    def __str__(self):
        return self.deptName
