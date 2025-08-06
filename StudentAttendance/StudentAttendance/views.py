from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from AttandanceData.models import AttandanceData
from django.contrib.auth.models import User,auth
from pyuploadcare import Uploadcare
import tempfile
import os
uc = Uploadcare(public_key='a5d4be2190a718075996', secret_key='c3445e533e8713336613')
def homepage(request):
    if request.user.is_authenticated:
        return render(request,"home.html")
    else:
        return HttpResponse("pls login")

def mainpage(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            a=request.POST["lecture"]
            b=request.POST["faculty"]
            c=request.POST["lecture_notes"]
            if 'file' in request.FILES:
                uploaded_file = request.FILES['file']
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
                    for chunk in uploaded_file.chunks():
                        temp_file.write(chunk)
                    temp_path = temp_file.name  # store path before it closes
                try:
                    # Step 2: Reopen it in read mode and upload
                    with open(temp_path, 'rb') as f:
                        result = uc.upload(f)
                    # Step 3: Save the file URL
                    file_url = result.cdn_url
                finally:
                    # Step 4: Cleanup temp file manually
                    if os.path.exists(temp_path):
                        os.remove(temp_path)
                e=request.user.username
                print(a,b,c,file_url,e)
                data=AttandanceData(lecture=a,faculty=b,lecture_notes=c,file=file_url,enrollment=e)
                data.save()
                return HttpResponseRedirect("/mainpage/")
    # You can now handle the uploaded file
            else:
    # No file was uploaded
                uploaded_file = "/homepage"
                e=request.user.username
                data=AttandanceData(lecture=a,faculty=b,lecture_notes=c,file=uploaded_file,enrollment=e)
                data.save()
                return HttpResponseRedirect("/mainpage/")
            #if uploaded_file is not None:
        # St#ep 1: Write the file to a temp file (do not auto-delete!)
            #    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[-1]) as temp_file:
            #        for chunk in uploaded_file.chunks():
            #            temp_file.write(chunk)
            #        temp_path = temp_file.name  # store path before it closes
            #    try:
            #        # Step 2: Reopen it in read mode and upload
            #        with open(temp_path, 'rb') as f:
            #            result = uc.upload(f)
            #        # Step 3: Save the file URL
            #        file_url = result.cdn_url
            #    finally:
            #        # Step 4: Cleanup temp file manually
            #        if os.path.exists(temp_path):
            #            os.remove(temp_path)
            #    e=request.user.username
            #    print(a,b,c,file_url,e)
            #    data=AttandanceData(lecture=a,faculty=b,lecture_notes=c,file=file_url,enrollment=e)
            #    data.save()
            #    return HttpResponseRedirect("/mainpage/")
            #else:
            #    uploaded_file = "opps"
            #    data=AttandanceData(lecture=a,faculty=b,lecture_notes=c,file=file_url,enrollment=e)
            #    data.save()
            #    return HttpResponseRedirect("/mainpage/")
        if request.method=="GET":
            return render(request,"details.html")

        return render(request,"details.html")
    else:
        return HttpResponse("pls login first")

def showdata(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            e=request.POST["enrollment"]
            data1=AttandanceData.objects.filter(enrollment=e)
            print(data1)
            return render(request,"showdata.html",{"data":data1})
        return render(request,'showdata.html')
    else:
        return HttpResponse("pls login")


def login(request):
    if request.method=="POST":
        e=request.POST["enrollment"]
        p=request.POST["password"]
        user=auth.authenticate(username=e,password=p)
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect("/homepage/")
        else:
            return HttpResponse("incorrect username and password")
    if request.method=="GET":
        return render(request,"login.html")
    return render(request,"login.html")

def signup(request):
    if request.method=="POST":
        u=request.POST["enrollment"]
        e=request.POST["email"]
        p=request.POST["password"]
        data=User.objects.create_user(username=u,email=e,password=p)
        data.save()
        return HttpResponseRedirect("/")
    if request.method=="GET":
        return render(request,"signup.html")
    return render(request,"signup.html")

def logout(request):
    auth.logout(request)
    return render(request,"login.html")