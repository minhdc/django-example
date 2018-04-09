from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.core.files import File

from .forms import EmailUploadForm
from .models import Email
# Create your views here.
def model_form_upload(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST,request.FILES)
        emails = request.FILES.getlist('file_field')
        if form.is_valid():
            for each_mail in emails:
                Email.objects.create(content = each_mail)
            return redirect('/uploader')
    else:
        form = EmailUploadForm()
    return render(request,'uploader/upload_form.html',{'form':form})

def home(request):
    emails = Email.objects.all()
    return render(request,'uploader/home.html',{'emails':emails})
