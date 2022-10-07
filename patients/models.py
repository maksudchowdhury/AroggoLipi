from django.db import models
from django.db.models.base import Model

from aroggo_lipi.settings import BASE_DIR
import os

# Create your models here.
# userLogin model
# userRegister model


class patientsInfo(models.Model):
    patientName = models.CharField(max_length=100)
    patientNID = models.IntegerField()
    patientDOB = models.DateField()
    patientPhone = models.CharField(max_length=20)
    patientEmail = models.CharField(max_length=50)
    patientPassword = models.TextField()
    patientImage = models.ImageField(upload_to=os.path.join(
        BASE_DIR, 'static/patientsUploadedImage'))

    def __str__(self):
        return self.patientName


class currentStatus(models.Model):
    patientEmail = models.CharField(max_length=50, default=False)
    visitingDate = models.DateField()
    bloodPressure = models.CharField(max_length=10)
    temperature = models.CharField(max_length=10)
    pulse = models.CharField(max_length=10)


class chiefComplain(models.Model):
    patientEmail = models.CharField(max_length=50, default=False)
    visitingDate = models.DateField()
    complain = models.CharField(max_length=100)


class diagnosis(models.Model):
    patientEmail = models.CharField(max_length=50, default=False)
    visitingDate = models.DateField()
    diagnosis = models.CharField(max_length=100)


class medicine(models.Model):
    patientEmail = models.CharField(max_length=50, default=False)
    visitingDate = models.DateField()
    medicineName = models.CharField(max_length=100)
    dose1 = models.CharField(max_length=10)
    dose2 = models.CharField(max_length=10)
    dose3 = models.CharField(max_length=10)
    duration = models.CharField(max_length=10)


class instruction(models.Model):
    patientEmail = models.CharField(max_length=50, default=False)
    visitingDate = models.DateField()
    instruction = models.CharField(max_length=300)


class diagnosticTest(models.Model):
    patientEmail = models.CharField(max_length=50, default=False)
    visitingDate = models.DateField()
    diagTest = models.CharField(max_length=300)
