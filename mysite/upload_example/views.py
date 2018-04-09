from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .forms import DocumentForm
from .models import Document
# Create your views here.

def home(request):
    documents = Document.objects.all()
    return render(request,'upload_example/home.html',{'documents':documents})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'upload_example/simple_upload.html',{'uploaded_file_url':uploaded_file_url})
    return render(request,'upload_example/simple_upload.html')

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request,'upload_example/upload.html',{'form':form})
