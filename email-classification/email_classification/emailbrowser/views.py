from django.shortcuts import render

from uploader.models import Email
# Create your views here.
def home(request):
    emails = Email.objects.all()
    return render(request,'emailbrowser/home.html',{'emails':emails})
