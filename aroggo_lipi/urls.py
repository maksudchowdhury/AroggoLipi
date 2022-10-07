"""aroggo_lipi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from doctors import views as doctor_views
from patients import views as patients_views
from healthcare import views as healthcare_views

urlpatterns = [
    path('admin/', admin.site.urls, name='adminPanel'),
    path('', patients_views.userLoginPage, name='userLoginPage'),
    path('userLoginProcess/', patients_views.userLoginProcess,
         name='userLoginProcess'),
    path('userRegisterPage/', patients_views.userRegisterPage,
         name='userRegisterPage'),
    path('userRegisterProcess/', patients_views.userRegisterProcess,
         name='userRegisterProcess'),
    path('doctors/', doctor_views.docLoginPage, name='docLoginPage'),
    path('docLoginProcess/', doctor_views.docLoginProcess, name='docLoginProcess'),
    path('docRegister/', doctor_views.docRegisterPage, name='docRegisterPage'),
    path('docRegisterProcess/', doctor_views.docRegisterProcess,
         name='docRegisterProcess'),

    path('healthcare/', healthcare_views.healthcareLoginPage,
         name='healthcareLoginPage'),
    path('healthcareLoginProcess/', healthcare_views.healthcareLoginProcess,
         name='healthcareLoginProcess'),
    path('panelRequest/',
         healthcare_views.panelRequest, name='panelRequest'),

    path('patientSelectProcess/',
         doctor_views.patientSelectProcess, name='patientSelectProcess'),


    path('savePatientStatus/',
         doctor_views.savePatientStatus, name='savePatientStatus'),
    path('deletePatientStatus/',
         doctor_views.deletePatientStatus, name='deletePatientStatus'),
    path('editPatientStatus/',
         doctor_views.editPatientStatus, name='editPatientStatus'),

    path('savePatientComplain/',
         doctor_views.savePatientComplain, name='savePatientComplain'),
    path('deletePatientComplain/',
         doctor_views.deletePatientComplain, name='deletePatientComplain'),
    path('editPatientComplain/',
         doctor_views.editPatientComplain, name='editPatientComplain'),


    path('savePatientDiagnosis/',
         doctor_views.savePatientDiagnosis, name='savePatientDiagnosis'),
    path('deletePatientDiagnosis/',
         doctor_views.deletePatientDiagnosis, name='deletePatientDiagnosis'),
    path('editPatientDiagnosis/',
         doctor_views.editPatientDiagnosis, name='editPatientDiagnosis'),



    path('savePatientTest/',
         doctor_views.savePatientTest, name='savePatientTest'),
    path('deletePatientTest/',
         doctor_views.deletePatientTest, name='deletePatientTest'),
    path('editPatientTest/',
         doctor_views.editPatientTest, name='editPatientTest'),

    path('savePatientInstruction/',
         doctor_views.savePatientInstruction, name='savePatientInstruction'),
    path('deletePatientInstruction/',
         doctor_views.deletePatientInstruction, name='deletePatientInstruction'),
    path('editPatientInstruction/',
         doctor_views.editPatientInstruction, name='editPatientInstruction'),

    path('savePatientMedicine/',
         doctor_views.savePatientMedicine, name='savePatientMedicine'),
    path('deletePatientMedicine/',
         doctor_views.deletePatientMedicine, name='deletePatientMedicine'),
    path('editPatientMedicine/',
         doctor_views.editPatientMedicine, name='editPatientMedicine'),

]
