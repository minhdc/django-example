import os
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.core.files import File

from .forms import EmailUploadForm
from .models import Email
from .utils import count_eml_files, do_the_classification_job, count_directory, get_list_of_current_dirs, get_list_of_incoming_emails


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
    ''' '''
    input_eml_path = "temp-email-storage"
    backup_path = "backup-emails"
    main_path = "mainstore"
    eml_key_to_search = "From"

    emails_info_in_db = Email.objects.all()
    email_counts = count_eml_files(input_eml_path)
    backed_up_email_counts = count_eml_files(backup_path)
    email_dir_counts = count_directory(main_path)

    do_the_classification_job(input_eml_path,backup_path,eml_key_to_search)

    current_dirs_list = get_list_of_current_dirs("mainstore")
    emails_in_dir = []
    dict_of_emails = {}
    #get list of emails in current dir - buggy!!! need to reset email list
    for each_dir in current_dirs_list:
        emails_in_dir.append(get_list_of_incoming_emails(os.path.join(main_path,each_dir)))                
        dict_of_emails.update({each_dir:emails_in_dir})        
        emails_in_dir = []    

    return render(request,'uploader/home.html',{'current_dirs_list':current_dirs_list,'dict_of_emails':dict_of_emails})


def emails_in_dir(request):
    ''''''
    main_path = "mainstore"
    current_dirs_list = get_list_of_current_dirs("mainstore")
    emails_in_dir = []
    for each_dir in current_dirs_list:
        emails_in_dir.append(get_list_of_incoming_emails(os.path.join(main_path,each_dir)))
        print("emails: ",get_list_of_incoming_emails(os.path.join(main_path,each_dir)))

    return render(request,'uploader/emails_in_dir.html',{'emails_in_dir':emails_in_dir})