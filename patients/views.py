import hashlib
from patients.models import patientsInfo, currentStatus, chiefComplain, diagnosis, medicine, instruction, diagnosticTest
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.


def userLoginPage(request):
    return render(request, 'userLogin.html')


def userLoginProcess(request):
    alert = ''
    patientEmail = request.POST.get('patientEmail')
    patientPassword = request.POST.get('patientPassword')
    visitingDate = request.POST.get('visitingDate')
    hashPass = str(hashlib.md5(patientPassword.encode("utf-8")).hexdigest())
    findPatientEntry = patientsInfo.objects.filter(
        patientEmail=patientEmail, patientPassword=hashPass).count()

    if(not findPatientEntry):
        alert = 'Wrong Credentials, Please enter the correct information'
        messages.info(request, alert)
        return redirect('userLoginPage')
    else:
        patientDataFromDB = patientsInfo.objects.get(
            patientEmail=patientEmail)
        patientCurrentStatusFromDB = currentStatus.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientChiefComplain = chiefComplain.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientDiagnosis = diagnosis.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientMedicine = medicine.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientInstruction = instruction.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientDiagTest = diagnosticTest.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)

        patientInformations = {'patientDetails': patientDataFromDB, 'currentStatus': patientCurrentStatusFromDB,
                               'complain': patientChiefComplain, 'diagnosis': patientDiagnosis, 'medicine': patientMedicine, 'instruction': patientInstruction, 'visitingDate': visitingDate, 'patientDiagTest': patientDiagTest}

        patientImageFileName = str(
            patientInformations['patientDetails'].patientImage).split('/')[-1]

        patientInformations.update(
            {'patientImageFileName': patientImageFileName})

        return render(request, 'patientPanel.html', patientInformations)


def userRegisterPage(request):

    return render(request, 'userRegister.html')


def userRegisterProcess(request):
    alert = ''
    saveRecord = patientsInfo()
    patientName = request.POST.get('patientName')
    patientNID = request.POST.get('patientNID')
    patientDOB = request.POST.get('patientDOB')
    patientPhone = request.POST.get('patientPhone')
    patientEmail = request.POST.get('patientEmail')
    patientPassword = request.POST.get('patientPassword')
    patientCPassword = request.POST.get('patientCPassword')

    hashPass = str(hashlib.md5(patientPassword.encode("utf-8")).hexdigest())
    patientImage = request.FILES['patientImage']

    checkPatientNID = patientsInfo.objects.filter(
        patientNID=patientNID).count()
    checkPatientEmail = patientsInfo.objects.filter(
        patientEmail=patientEmail).count()
    if(checkPatientNID > 0 or checkPatientEmail > 0 or patientPassword != patientCPassword):
        if(checkPatientNID > 0 and checkPatientEmail > 0):
            alert = 'The email address and the NID number you entered has already been registered'
        elif(checkPatientNID > 0):
            alert = 'The NID number you entered has already been registered'
        elif(checkPatientEmail > 0):
            alert = 'The email address you entered has already been registered'
        else:
            alert = 'The passwords are not matching'

        messages.info(request, alert)
        return redirect('userRegisterPage')

    if(checkPatientEmail > 0):
        messages.success(request, 'Email already exists')

    print(checkPatientEmail, checkPatientNID)

    if request.method == 'POST' and checkPatientNID == 0 and checkPatientEmail == 0:
        saveRecord.patientName = patientName
        saveRecord.patientNID = patientNID
        saveRecord.patientDOB = patientDOB
        saveRecord.patientPhone = patientPhone
        saveRecord.patientEmail = patientEmail
        saveRecord.patientPassword = hashPass
        saveRecord.patientImage = patientImage
        saveRecord.save()
        return HttpResponse("Thanks for signing up")
        # return HttpResponse("Welcome SIGNED IN")

    else:

        return HttpResponse("NOT POST METHOD")
