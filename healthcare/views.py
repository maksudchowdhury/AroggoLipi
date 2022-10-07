from django.http.response import HttpResponse
from django.shortcuts import render
from healthcare.models import doc_reg_info, healthcareCenter
from django.shortcuts import redirect
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def healthcareLoginPage(request):
    return render(request, 'healthcareLogin.html')


def healthcareLoginProcess(request):
    alert = ''
    centerName = request.POST.get('centerName')
    centerPassword = request.POST.get('centerPassword')
    # hashPass = str(hashlib.md5(docPassword.encode("utf-8")).hexdigest())
    findCenterEntry = healthcareCenter.objects.filter(
        centerName=centerName, centerPassword=centerPassword).count()

    if(not findCenterEntry):
        alert = 'Wrong Credentials, Please enter the correct information'
        messages.info(request, alert)
        return redirect('healthcareLoginPage')
    else:
        panelInformation = doc_reg_info.objects.filter(
            docHospital=centerName, accountStatus='pending')

        approvePanelTable = {
            'panelInformation': panelInformation, 'centerName': centerName}

        # return render(request, 'patientPanel.html', patientInformations)
        # return HttpResponse("THE DOCTORS VIEW PANEL IS UNDER CONSTRUCTION")
        return render(request, 'approvePanel.html', approvePanelTable)


def panelRequest(request):
    docid = ''
    centerName = ''
    acceptAction = str(request.POST.get('accept'))
    declineAction = str(request.POST.get('decline'))
    centerName = str(request.POST.get('panelRequest'))
    print(centerName)
    if(acceptAction != 'None'):
        acceptActions = acceptAction.split('_')
        docid = acceptActions[1]
        centerName = acceptActions[2]
        docObject = doc_reg_info.objects.get(id=docid)
        docNID = docObject.docNID
        docObject.accountStatus = 'approved'
        docObject.save()
        docOtherReq = doc_reg_info.objects.filter(
            docNID=docNID, accountStatus='pending').exclude(id=docid)
        docOtherReq.delete()

    elif(declineAction != 'None'):
        declineActions = declineAction.split('_')
        docid = declineActions[1]
        centerName = declineActions[2]
        docObject = doc_reg_info.objects.get(id=docid)
        docObject.delete()

    panelInformation = doc_reg_info.objects.filter(
        docHospital=centerName, accountStatus='pending')
    approvePanelTable = {
        'panelInformation': panelInformation, 'centerName': centerName}
    return render(request, 'approvePanel.html', approvePanelTable)
