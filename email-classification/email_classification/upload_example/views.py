from django.shortcuts import render,redirect

from .forms import EmailUploadForm
from .models import Email
# Create your views here.
def model_form_upload(request):
    if request.method == 'POST':
        form = EmailUploadForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/upload')
    else:
        form = EmailUploadForm()
    return render(request, 'upload_example/model_form_upload.html',{'form':form})

def home(request):
    emails = Email.objects.all()
    return render(request, 'upload_example/home.html', { 'emails': emails })
