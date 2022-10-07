from django.http.response import HttpResponse
from django.shortcuts import render
from healthcare.models import doc_reg_info
from healthcare.models import healthcareCenter
from healthcare.models import healthcareDepartment
from django.shortcuts import redirect
from django.contrib import messages
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
        docEmail=docEmail, docPassword=hashPass).count()

    if(not findDocEntry):
        alert = 'Wrong Credentials, Please enter the correct information'
        messages.info(request, alert)
        return redirect('docLoginPage')
    else:
        # docDataFromDB = doc_reg_info.objects.get(
        #     docEmail=docEmail)

        # docInformations = {'docDetails': docDataFromDB}

        # docImageFileName = str(
        #     docInformations['docDetails'].docImage).split('/')[-1]

        # docInformations.update(
        #     {'docImageFileName': docImageFileName})

        # return render(request, 'patientPanel.html', patientInformations)
        print('this file is working up until here')
        return HttpResponse("THE DOCTORS VIEW PANEL IS UNDER CONSTRUCTION")


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

    checkDocNID = doc_reg_info.objects.filter(
        docNID=docNID).count()
    checkDocEmail = doc_reg_info.objects.filter(
        docEmail=docEmail).count()
    if(checkDocNID > 0 or checkDocEmail > 0 or docPassword != docCPassword):
        if(checkDocNID > 0 and checkDocEmail > 0):
            alert = 'The email address and the NID number you entered has already been registered'
        elif(checkDocNID > 0):
            alert = 'The NID number you entered has already been registered'
        elif(checkDocEmail > 0):
            alert = 'The email address you entered has already been registered'
        else:
            alert = 'The Passwords are not matching'

        messages.info(request, alert)
        return redirect('docRegisterPage')

    if request.method == 'POST' and checkDocNID == 0 and checkDocEmail == 0:
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
