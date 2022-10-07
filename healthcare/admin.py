from django.contrib import admin
from healthcare import models
# Register your models here.
admin.site.register(models.doc_reg_info)
admin.site.register(models.healthcareCenter)
admin.site.register(models.healthcareDepartment)
