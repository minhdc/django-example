import os
import quopri
import shutil
import base64

from email import message_from_file
from .attachment_extractor import has_attachment, get_multiple_attachment, write_multiple_attachment, get_email_subject


def count_eml_files(path):
    ''' 
        calculate the number of *.eml files in current dir
    '''
    email_counts = 0
    for each_element in os.listdir(path):
        if each_element.endswith(".eml"):
            email_counts += 1
    return email_counts


def count_directory(path):
    '''
        calculate the number of directories in current path
    '''
    dir_counts = 0
    for each_element in os.listdir(path):
        if os.path.isdir(each_element):
            dir_counts += 1
    return dir_counts


def get_email_object(path_to_eml_file, file_name):
    ''' 
        return an email_object with ISO-8859-1 encoding type
    '''
    return message_from_file(open(path_to_eml_file+os.sep+file_name, "r", encoding="ISO-8859-1"))


def extract_value_in_header(email_object, header_key_to_extract):
    '''
        get the corresponding value of any provided key in the eml header
        ...and sanitize it to match the need
        ... in this case: "From" address with <whoami>
    '''
    email_header_value = email_object[header_key_to_extract]
    try:
        start_point = email_header_value.index('<')
        stop_point = email_header_value.index('>')
    except ValueError as verr:
        return "shit"
    from_address_in_header = []
    for i in range(start_point+1, stop_point):
        from_address_in_header.append(email_header_value[i])
    #print("header: ")
    print(''.join(from_address_in_header))
    return ''.join(from_address_in_header)


def extract_from_address_in_payload(email_object, header_key_to_extract):
    '''
        return the "From" address in the payload of an eml file
    '''
    start_point = 0
    stop_point = 0

    email_payload_as_string = str(email_object.get_payload()[0])

    try:
        start_point = email_payload_as_string.index('<')
        stop_point = email_payload_as_string.index('>')
        # buggy way to handle tags
        if (stop_point - start_point) >= 40:
            return extract_value_in_header(email_object, "From")
    except (ValueError, OSError) as verr:
        print(verr)

    extracted_from_address = []
    for i in range(start_point+1, stop_point):
        extracted_from_address.append(email_payload_as_string[i])
    if '@' not in extracted_from_address:
        return extract_value_in_header(email_object, "From")
    #print("payload: ")
    #print(''.join(extracted_from_address))
    # bad solution to remove newline character in from address string
    result = ''.join(extracted_from_address)
    result = result.strip('\n')
    return result


def get_list_of_incoming_emails(current_eml_path):
    ''' 
        return a list of names of emails in the current path
    '''
    email_list = []
    for each_element in os.listdir(current_eml_path):
        if each_element.endswith(".eml"):
            email_list.append(each_element)    
    #print("email list = ",email_list)
    return email_list


def get_eml_header(input_file_path):
    ''' 
        return the header of an eml file
    '''
    input_file_as_path = open(input_file_path, "r")
    return message_from_file(input_file_path)._headers


def get_value_by_key(eml_header, key_to_search):
    '''
        return exactly the fullest-corresponding value of any provided key in eml header
    '''
    for key, value in eml_header:
        if key == key_to_search:
            return value
    return None


def get_email_addr_from_obfuscated_string(obfuscated_string):
    '''
        deprecated
    '''
    email_address = []
    start_point = obfuscated_string.index("<")+1
    stop_point = obfuscated_string.index(">")
    for i in range(start_point, stop_point):
        email_address.append(obfuscated_string[i])

    if not email_address:
        return None
    return ''.join(email_address)


def create_email_storing_folder_if_not_exists(folder_name, folder_path):
    '''
        create a folder to copy eml file in
    '''
    try:
        check = os.listdir(os.path.join(folder_path, folder_name))
        if check:
            print("")
            #print("folder %s already exists"%folder_name)
    except FileNotFoundError as err:
        os.mkdir(os.path.join(folder_path, folder_name))
        print("created storing folder %s at %s" % (folder_name, os.getcwd()))


def copy_email_to_storing_folder(src, dst, email_file_name):
    ''' 
        just doin the copycat jjob
    '''
    if not os.path.isfile(email_file_name):
        try:
            shutil.copy2(os.path.join(src, email_file_name), os.path.join(dst, email_file_name))
            #need to update new location to current_loc field in email database
            #
            #
            #
            #
        except shutil.Error as e:
            print("shutil error in copyin email to storing folder")            
    else:
        print("already exists")


def move_copied_email_to_treasure(src, treasure_path, email_file_name, dst=None):
    '''
        now, inside a bunker
    '''
    create_email_storing_folder_if_not_exists(treasure_path, "")
    try:
        shutil.move(os.path.join(src, email_file_name), treasure_path)
    except shutil.Error as e:
        print("")
        # print("dup")


def get_message_content_in_email_file(main_store, email_file_name):
    '''
        return the message as plain text
    '''
    email_object = message_from_file(open(os.path.join(main_store, email_file_name), "r"))
    if email_object.is_multipart():
        for each_element in email_object.walk():
            if each_element.get_content_type() == "text/plain":
                return each_element.get_payload()
    return None


def create_folder_for_this_mail(email_object, current_storing_path):
    folder_name = ""
    for k, v in email_object._headers:
        if k == "Subject":
            folder_name = v
    try:
        check = os.listdir(os.path.join(current_storing_path, folder_name))
        if check:
            print("current folder exists")
    except FileNotFoundError as err:
        os.mkdir(os.path.join(current_storing_path, folder_name))
        #print("created storing folder %s at %s" % (folder_name, os.getcwd()))


def do_the_classification_job(current_eml_path, treasure_path, eml_key_to_search):
    '''
        powerlifting
    '''
    email_list = get_list_of_incoming_emails(current_eml_path)

    if email_list is not None:
        for each_mail in email_list:
            #from_addr = extract_from_address_in_payload(get_email_object(current_eml_path,each_mail),"From")
            from_addr = extract_value_in_header(get_email_object(current_eml_path, each_mail), "From")
            create_email_storing_folder_if_not_exists(from_addr, "mainstore")
            copy_email_to_storing_folder(current_eml_path, os.path.join("mainstore", from_addr), each_mail)
          
            move_copied_email_to_treasure(current_eml_path, treasure_path, each_mail)
    else:
        print("empty email list")


def process_attachment(current_eml_path):
    '''
        attachment processor: extract then create a folder with name = eml_file_name, then copy all into it.
    '''
    email_list = get_list_of_incoming_emails(current_eml_path)
    print("email-list",email_list)
    try:
        for each_mail in email_list:
            email_object = message_from_file(open(os.path.join(current_eml_path, each_mail), "r"))
            if has_attachment(email_object._headers):
                list_attachment = get_multiple_attachment(email_object)
                write_multiple_attachment(list_attachment, current_eml_path, each_mail.strip(".eml"))
                #need to count the number of attachments then update in to attachment_number in database field
                #
                #
                #
                try:
                    shutil.move(os.path.join(current_eml_path, each_mail), os.path.join(current_eml_path,each_mail.strip(".eml")))
                except shutil.Error as e:
                    print("move eml error")
                    print("got 1 attachment")                
    except TypeError as err:
        print("type error while processing attachment")
        pass
    # move eml to folder
    

def get_list_of_current_dirs(current_path):
    ''' [NOT COMPLETED] 
    list dirs in current path. 
    '''
    current_dirs = []
    for each_element in os.listdir(current_path):
            if os.path.isdir(os.path.join(current_path,each_element)):
                current_dirs.append(each_element)
    return current_dirs
