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

    
    root_dirs_list = get_list_of_current_dirs("mainstore")    # root = 1st dir list 
    list_of_2nd_dirs = []
    list_of_3rd_dirs = []
    dict_of_emails = {}
    email_in_dir = {}
    #get list of emails in current dir - buggy!!! need to reset email list
    for each_1st_dir in root_dirs_list:            
        list_of_2nd_dirs = get_list_of_current_dirs(os.path.join(main_path,each_1st_dir))
        list_of_2nd_dirs = list_of_2nd_dirs + (get_list_of_incoming_emails(os.path.join(main_path,each_1st_dir)))    
        #look for attachment...
        for each_2nd_dir in list_of_2nd_dirs:            
            if ".eml" not in each_2nd_dir:
                list_of_3rd_dirs = os.listdir(os.path.join(main_path,os.path.join(each_1st_dir,each_2nd_dir)))
                #if get_list_of_incoming_emails(os.path.join(main_path,os.path.join(each_1st_dir,each_2nd_dir))):
                #    list_of_3rd_dirs.append(get_list_of_incoming_emails(os.path.join(main_path,os.path.join(each_1st_dir,each_2nd_dir))))                      
                email_in_dir[each_2nd_dir]=[list_of_3rd_dirs]            
                             
            if each_1st_dir in dict_of_emails:
                if email_in_dir:
                    dict_of_emails[each_1st_dir].append(email_in_dir)            
                else:
                    dict_of_emails[each_1st_dir].append(each_2nd_dir)
            else:
                if email_in_dir:
                    dict_of_emails[each_1st_dir] = [email_in_dir]
                else:
                    dict_of_emails[each_1st_dir] = each_2nd_dir

            print("\n\n--------")
            print("dict of email ",dict_of_emails)
            print("--------\n\n")
            #reset            
            email_in_dir = {}
            list_of_3rd_dirs = []


    print("root dir list: ",root_dirs_list)                                                                                                                                                
    return render(request,'uploader/home.html',{'current_dirs_list':root_dirs_list,'dict_of_emails':dict_of_emails})


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
    
    return HttpResponse(dirs_in_dir)