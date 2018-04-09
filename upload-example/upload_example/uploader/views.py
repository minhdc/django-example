from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import UploadFileForm
# Create your views here.

#import something to handle upload file here
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            #handle here
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request,'upload.html',{'form':form})
