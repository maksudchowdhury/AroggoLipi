from django.http.response import HttpResponse
from django.shortcuts import render
from healthcare.models import doc_reg_info
from healthcare.models import healthcareCenter
from healthcare.models import healthcareDepartment
from patients.models import patientsInfo, currentStatus, chiefComplain, diagnosis as diagnosisDB, medicine as medicineDB, instruction as instructionDB, diagnosticTest as testDB
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib

# Create your views here.


def docLoginPage(request):
    return render(request, 'docLogin.html')


def docLoginProcess(request):
    alert = ''
    docEmail = request.POST.get('docEmail')
    docPassword = str(request.POST.get('docPassword'))
    hashPass = str(hashlib.md5(docPassword.encode("utf-8")).hexdigest())
    findDocEntry = doc_reg_info.objects.filter(
        docEmail=docEmail, docPassword=hashPass,accountStatus="approved").count()

    if(not findDocEntry):
        alert = 'Wrong Credentials or Account is not approved yet'
        messages.info(request, alert)
        return redirect('docLoginPage')

    else:

        docDataFromDB = doc_reg_info.objects.get(
            docEmail=docEmail)

        docInformations = {'docDetails': docDataFromDB}

        return render(request, 'rxPanel.html', docInformations)


def docRegisterPage(request):
    healthcareCenterNameFromDB = healthcareCenter.objects.only('centerName')
    healthcareDepartmenFromDB = healthcareDepartment.objects.only('deptName')
    docInformations = {'docHospital': healthcareCenterNameFromDB,
                       'docDepartment': healthcareDepartmenFromDB}
    print(docInformations['docHospital'])
    return render(request, 'docRegister.html', docInformations)


def docRegisterProcess(request):
    alert = ''
    saveRecord = doc_reg_info()
    docName = request.POST.get('docName')
    docNID = request.POST.get('docNID')
    docDOB = request.POST.get('docDOB')
    docHospital = request.POST.get('docHospital')
    docDepartment = request.POST.get('docDepartment')
    docEID = request.POST.get('docEID')
    docPhone = request.POST.get('docPhone')
    docEmail = request.POST.get('docEmail')
    docPassword = request.POST.get('docPassword')
    docCPassword = request.POST.get('docCPassword')

    hashPass = str(hashlib.md5(docPassword.encode("utf-8")).hexdigest())
    docImage = request.FILES['docImage']

    checkDocApprove = doc_reg_info.objects.filter(
        docNID=docNID, accountStatus='approved').count()
    checkDocEmail = doc_reg_info.objects.filter(
        docEmail=docEmail).count()
    # checkDocEmail = doc_reg_info.objects.filter(
    #     docEmail=docEmail).count()
    if(checkDocApprove > 0 or docPassword != docCPassword or checkDocEmail > 0):
        if(checkDocApprove > 0):
            alert = 'Account with this NID has already been registered'
        elif(docPassword != docCPassword):
            alert = 'The Passwords are not matching'
        else:
            alert = 'Account with email has already been registered'
        messages.info(request, alert)
        return redirect('docRegisterPage')

    if request.method == 'POST' and checkDocApprove == 0:
        saveRecord.docName = docName
        saveRecord.docNID = docNID
        saveRecord.docDOB = docDOB
        saveRecord.docHospital = docHospital
        saveRecord.docDepartment = docDepartment
        saveRecord.docEID = docEID
        saveRecord.docPhone = docPhone
        saveRecord.docDepartment = docDepartment
        saveRecord.docEmail = docEmail
        saveRecord.docPassword = hashPass
        saveRecord.docImage = docImage
        saveRecord.save()

        docHospitalName = {'centerName': docHospital}
        return render(request, 'docRegister2.html', docHospitalName)
        # return HttpResponse("Welcome SIGNED IN")

    else:

        return HttpResponse("NOT POST METHOD")


def patientSelectProcess(request):
    patientEmail = str(request.POST.get('patientEmail'))
    visitingDate = request.POST.get('visitingDate')

    findPatient = patientsInfo.objects.filter(
        patientEmail=patientEmail).count()

    if(findPatient == 0 or visitingDate == ""):
        alert = 'Please enter valid information'
        messages.info(request, alert)
        return render(request, 'rxPanel.html')

    else:

        patientDataFromDB = patientsInfo.objects.get(
            patientEmail=patientEmail)
        patientCurrentStatusFromDB = currentStatus.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientChiefComplain = chiefComplain.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientDiagnosis = diagnosisDB.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientMedicine = medicineDB.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientInstruction = instructionDB.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)
        patientDiagTest = testDB.objects.filter(
            patientEmail=patientEmail, visitingDate=visitingDate)

        patientInformations = {'patientDetails': patientDataFromDB, 'currentStatus': patientCurrentStatusFromDB, 'patientEmail': patientEmail,
                               'complain': patientChiefComplain, 'diagnosis': patientDiagnosis, 'medicine': patientMedicine, 'instruction': patientInstruction, 'visitingDate': visitingDate, 'patientDiagTest': patientDiagTest, 'patientSelected': True}

        patientImageFileName = str(
            patientInformations['patientDetails'].patientImage).split('/')[-1]

        patientInformations.update(
            {'patientImageFileName': patientImageFileName})

        return render(request, 'rxPanel.html', patientInformations)


def savePatientStatus(request):
    if request.method == 'POST':
        patientEmail = str(request.POST.get('patientEmail'))
        visitingDate = request.POST.get('visitingDate')

        bp = request.POST.get('bp')
        temp = request.POST.get('temp')
        pulse = request.POST.get('pulse')
        patientStatusID = str(request.POST.get('statusID'))
        print("printing statID", patientStatusID)
        if(patientStatusID == ""):
            currentStatusObj = currentStatus(
                patientEmail=patientEmail, visitingDate=visitingDate, bloodPressure=bp, temperature=temp, pulse=pulse)
            currentStatusObj.save()
        else:
            print("executing this section and bp is ", bp)
            currentStatusObj = currentStatus.objects.get(id=patientStatusID)
            currentStatusObj.bloodPressure = bp
            currentStatusObj.temperature = temp
            currentStatusObj.pulse = pulse
            currentStatusObj.save()
        currentStatusTable = list(currentStatus.objects.filter(
            visitingDate=visitingDate, patientEmail=patientEmail).values())

        return JsonResponse({'status': 'saved', 'currentStatusTable': currentStatusTable})
    else:
        return JsonResponse({'status': 0})


def deletePatientStatus(request):
    if request.method == 'POST':
        infoID = str(request.POST.get('id'))
        if(infoID != ""):
            statusInfo = currentStatus.objects.filter(id=infoID)
            statusInfo.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'status': 0})


def editPatientStatus(request):
    if request.method == 'POST':
        infoID = str(request.POST.get('id'))
        if(infoID != ""):
            statusInfo = list(currentStatus.objects.filter(id=infoID).values())
            print(statusInfo)

        return JsonResponse({'status': 'edited', 'currentStatusRow': statusInfo})
    else:
        return JsonResponse({'status': 0})


def savePatientComplain(request):
    if request.method == 'POST':
        patientEmail = str(request.POST.get('patientEmail'))
        visitingDate = request.POST.get('visitingDate')

        complain = request.POST.get('complain')
        complainID = str(request.POST.get('complainID'))

        if(complainID == ""):  # newEntry
            print("new entry, complain and complainID", complain, complainID)
            complainObj = chiefComplain(
                patientEmail=patientEmail, visitingDate=visitingDate, complain=complain)
            complainObj.save()
        else:  # update
            print("updated entry, complain and complainID", complain, complainID)
            complainObj = chiefComplain.objects.get(id=complainID)
            complainObj.complain = complain
            complainObj.save()
            print("complain updated")
        complainTable = list(chiefComplain.objects.filter(
            visitingDate=visitingDate, patientEmail=patientEmail).values())

        return JsonResponse({'status': 'saved', 'complainTable': complainTable})
    else:
        return JsonResponse({'status': 0})


def deletePatientComplain(request):
    if request.method == 'POST':
        complainID = str(request.POST.get('complainID'))
        if(complainID != ""):
            complainObj = chiefComplain.objects.filter(id=complainID)
            complainObj.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'status': 0})


def editPatientComplain(request):
    if request.method == 'POST':
        complainID = str(request.POST.get('complainID'))
        if(complainID != ""):
            complainObj = list(
                chiefComplain.objects.filter(id=complainID).values())
            print(complainObj)

        return JsonResponse({'status': 'edited', 'currentComplainRow': complainObj})
    else:
        return JsonResponse({'status': 0})


def savePatientDiagnosis(request):
    if request.method == 'POST':
        patientEmail = str(request.POST.get('patientEmail'))
        visitingDate = request.POST.get('visitingDate')

        diagnosis = request.POST.get('diagnosis')
        diagnosisID = str(request.POST.get('diagnosisID'))

        if(diagnosisID == ""):  # newEntry
            print("new entry, diagnosis and diagnosisID", diagnosis, diagnosisID)
            diagnosisObj = diagnosisDB(
                patientEmail=patientEmail, visitingDate=visitingDate, diagnosis=diagnosis)
            diagnosisObj.save()
        else:  # update
            print("updated entry, diagnosis and diagnosisID",
                  diagnosis, diagnosisID)
            diagnosisObj = diagnosisDB.objects.get(id=diagnosisID)
            diagnosisObj.diagnosis = diagnosis
            diagnosisObj.save()
            print("diagnosis updated")
        diagnosisTable = list(diagnosisDB.objects.filter(
            visitingDate=visitingDate, patientEmail=patientEmail).values())

        return JsonResponse({'status': 'saved', 'diagnosisTable': diagnosisTable})
    else:
        return JsonResponse({'status': 0})


def deletePatientDiagnosis(request):
    if request.method == 'POST':
        diagnosisID = str(request.POST.get('diagnosisID'))
        if(diagnosisID != ""):
            diagnosisObj = diagnosisDB.objects.filter(id=diagnosisID)
            diagnosisObj.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'status': 0})


def editPatientDiagnosis(request):
    if request.method == 'POST':
        diagnosisID = str(request.POST.get('diagnosisID'))
        if(diagnosisID != ""):
            diagnosisObj = list(
                diagnosisDB.objects.filter(id=diagnosisID).values())
            print(diagnosisObj)

        return JsonResponse({'status': 'edited', 'currentDiagnosisRow': diagnosisObj})
    else:
        return JsonResponse({'status': 0})


def savePatientTest(request):
    if request.method == 'POST':
        patientEmail = str(request.POST.get('patientEmail'))
        visitingDate = request.POST.get('visitingDate')

        test = request.POST.get('test')
        testID = str(request.POST.get('testID'))

        if(testID == ""):  # newEntry
            print("new entry, test and testID", test, testID)
            testObj = testDB(
                patientEmail=patientEmail, visitingDate=visitingDate, diagTest=test)
            testObj.save()
        else:  # update
            print("updated entry, test and testID",
                  test, testID)
            testObj = testDB.objects.get(id=testID)
            testObj.diagTest = test
            testObj.save()
            print("test updated")
        testTable = list(testDB.objects.filter(
            visitingDate=visitingDate, patientEmail=patientEmail).values())

        return JsonResponse({'status': 'saved', 'testTable': testTable})
    else:
        return JsonResponse({'status': 0})


def deletePatientTest(request):
    if request.method == 'POST':
        testID = str(request.POST.get('testID'))
        if(testID != ""):
            testObj = testDB.objects.filter(id=testID)
            testObj.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'status': 0})


def editPatientTest(request):
    if request.method == 'POST':
        testID = str(request.POST.get('testID'))
        if(testID != ""):
            testObj = list(
                testDB.objects.filter(id=testID).values())
            print(testObj)

        return JsonResponse({'status': 'edited', 'currentTestRow': testObj})
    else:
        return JsonResponse({'status': 0})


def savePatientInstruction(request):
    if request.method == 'POST':
        patientEmail = str(request.POST.get('patientEmail'))
        visitingDate = request.POST.get('visitingDate')

        instruction = request.POST.get('instruction')
        instructionID = str(request.POST.get('instructionID'))

        if(instructionID == ""):  # newEntry
            print("new entry, instruction and instructionID",
                  instruction, instructionID)
            instructionObj = instructionDB(
                patientEmail=patientEmail, visitingDate=visitingDate, instruction=instruction)
            instructionObj.save()
        else:  # update
            print("updated entry, instruction and instructionID",
                  instruction, instructionID)
            instructionObj = instructionDB.objects.get(id=instructionID)
            instructionObj.instruction = instruction
            instructionObj.save()
            print("instruction updated")
        instructionTable = list(instructionDB.objects.filter(
            visitingDate=visitingDate, patientEmail=patientEmail).values())

        return JsonResponse({'status': 'saved', 'instructionTable': instructionTable})
    else:
        return JsonResponse({'status': 0})


def deletePatientInstruction(request):
    if request.method == 'POST':
        instructionID = str(request.POST.get('instructionID'))
        if(instructionID != ""):
            instructionObj = instructionDB.objects.filter(id=instructionID)
            instructionObj.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'status': 0})


def editPatientInstruction(request):
    if request.method == 'POST':
        instructionID = str(request.POST.get('instructionID'))
        if(instructionID != ""):
            instructionObj = list(
                instructionDB.objects.filter(id=instructionID).values())
            print(instructionObj)

        return JsonResponse({'status': 'edited', 'currentInstructionRow': instructionObj})
    else:
        return JsonResponse({'status': 0})


def savePatientMedicine(request):
    if request.method == 'POST':
        patientEmail = str(request.POST.get('patientEmail'))
        visitingDate = request.POST.get('visitingDate')

        medicine = request.POST.get('medicine')
        medicineID = request.POST.get('medicineID')
        dose1 = str(request.POST.get('dose1'))
        dose2 = str(request.POST.get('dose2'))
        dose3 = str(request.POST.get('dose3'))
        duration = str(request.POST.get('duration'))
        print("this is medicine id", medicineID)

        if(medicineID == ""):  # newEntry
            print("new entry, medicine and medicineID",
                  medicine, medicineID)
            medicineObj = medicineDB(
                patientEmail=patientEmail, visitingDate=visitingDate, medicineName=medicine, dose1=dose1, dose2=dose2, dose3=dose3, duration=duration)
            medicineObj.save()
        else:  # update
            print("updated entry, medicine and medicineID",
                  medicine, medicineID)
            medicineObj = medicineDB.objects.get(id=medicineID)
            medicineObj.medicineName = medicine
            medicineObj.dose1 = dose1
            medicineObj.dose2 = dose2
            medicineObj.dose3 = dose3
            medicineObj.duration = duration

            medicineObj.save()
            print("medicine updated")
        medicineTable = list(medicineDB.objects.filter(
            visitingDate=visitingDate, patientEmail=patientEmail).values())

        return JsonResponse({'status': 'saved', 'medicineTable': medicineTable})
    else:
        return JsonResponse({'status': 0})


def deletePatientMedicine(request):
    if request.method == 'POST':
        medicineID = str(request.POST.get('medicineID'))
        if(medicineID != ""):
            medicineObj = medicineDB.objects.filter(id=medicineID)
            medicineObj.delete()
        return JsonResponse({'status': 'deleted'})
    else:
        return JsonResponse({'status': 0})


def editPatientMedicine(request):
    if request.method == 'POST':
        medicineID = str(request.POST.get('medicineID'))
        if(medicineID != ""):
            medicineObj = list(
                medicineDB.objects.filter(id=medicineID).values())
            print(medicineObj)

        return JsonResponse({'status': 'edited', 'currentMedicineRow': medicineObj})
    else:
        return JsonResponse({'status': 0})
