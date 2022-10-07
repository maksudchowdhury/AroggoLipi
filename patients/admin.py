from django.contrib import admin
from patients import models
# Register your models here.
admin.site.register(models.patientsInfo)
admin.site.register(models.currentStatus)
admin.site.register(models.chiefComplain)
admin.site.register(models.diagnosis)
admin.site.register(models.medicine)
admin.site.register(models.instruction)
admin.site.register(models.diagnosticTest)
