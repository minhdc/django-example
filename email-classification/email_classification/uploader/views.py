from django.shortcuts import render,redirect
from django.views.generic.edit import FormView
from django.core.files import File

from .forms import EmailUploadForm
from .models import Email
from .utils import count_eml_files,do_the_classification_job,count_directory
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
    input_eml_path = "temp-email-storage"
    backup_path = "backup-emails"
    main_path = "mainstore"
    eml_key_to_search = "From"

    emails_info_in_db = Email.objects.all()
    email_counts = count_eml_files(input_eml_path)
    backed_up_email_counts = count_eml_files(backup_path)
    email_dir_counts = count_directory(main_path)

    do_the_classification_job(input_eml_path,backup_path,eml_key_to_search)

    return render(request,'uploader/home.html')
