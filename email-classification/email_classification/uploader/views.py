import os

from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.core.files import File
from django.http import HttpResponse

from .forms import EmailUploadForm
from .models import Email
from .utils import count_eml_files, do_the_classification_job, count_directory, get_list_of_current_dirs, get_list_of_incoming_emails, get_message_content_in_email_file,process_attachment


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

    if count_eml_files(input_eml_path) != 0:
        do_the_classification_job(input_eml_path,backup_path,eml_key_to_search)

   
    current_dirs_list = get_list_of_current_dirs("mainstore")
    emails_in_dir = {}
    dirs_in_dir = []
    child_dirs_in_dir = []
    dict_of_emails = {}
    #get list of emails in current dir - buggy!!! need to reset email list
    for each_dir in current_dirs_list:
        #   emails_in_dir.append(get_list_of_incoming_emails(os.path.join(main_path,each_dir)))  
        dirs_in_dir = get_list_of_current_dirs(os.path.join(main_path,each_dir))
        for cdir in dirs_in_dir:
            child_dirs_in_dir.append(os.listdir(os.path.join(main_path,os.path.join(each_dir,cdir))))
            emails_in_dir.update({cdir:child_dirs_in_dir})
       
        dict_of_emails.update({each_dir:emails_in_dir})        
        #dict_of_emails.update({each_dir:dirs_in_dir})  
        emails_in_dir = []           

    return render(request,'uploader/home.html',{'current_dirs_list':current_dirs_list,'dict_of_emails':dict_of_emails})


def show_email_payload(request):
    ''' fvck this thing'''
    if request.method == "GET":
        main_path = "mainstore"
        file_name = request.GET["file_name"]
        parent = request.GET["parent"]
        print("email file name: ",file_name)
        email_payload = get_message_content_in_email_file(main_path,os.path.join(parent,file_name))
        return HttpResponse(email_payload,content_type="text/plain")
    else:        
        return HttpResponse("Request method isn't GET . Fvck yo")
        

def do_the_attachment_job(request):
    if request.method == "GET":
        main_path = "mainstore"
        folder_name = request.GET["folder_name"]
        process_attachment(os.path.join(main_path,folder_name))
        print("successed in attachment extraction")
        return HttpResponse("good")
    else:
        return HttpResponse("Request method isn't GET. fvckyooo")





def dirs_in_dir(request):
    ''''''
    main_path = "mainstore"
    dirs_in_dir = []
    if request.method == "GET":
        current_dir = request.GET["current_dir"]
        print("current_dir : ",current_dir)
        for each_element in os.listdir(os.path.join(main_path,current_dir)):
            if os.path.isdir(os.path.join(main_path,current_dir,each_element)):
                dirs_in_dir.append(each_element)
    
    return render(request,"uploader/home.html",{'dirs_in_dir':dirs_in_dir})