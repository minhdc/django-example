import os
import quopri
import shutil
import base64

from email import message_from_file

def count_eml_files(path):
    email_counts = 0
    for each_element in os.listdir(path):
        if each_element.endswith(".eml"):
            email_counts += 1;
    return email_counts


def count_directory(path):
    dir_counts = 0
    for each_element in os.listdir(path):
        if os.path.isdir(each_element):
            dir_counts += 1
    return dir_counts


def get_email_object(path_to_eml_file, file_name):
    return message_from_file(open(path_to_eml_file+os.sep+file_name, "r", encoding="ISO-8859-1"))


def extract_value_in_header(email_object, header_key_to_extract):
    email_header_value = email_object[header_key_to_extract]
    try:
        start_point = email_header_value.index('<')
        stop_point = email_header_value.index('>')
    except ValueError as verr:
        return "shit"
    from_address_in_header = []
    for i in range(start_point+1,stop_point):
        from_address_in_header.append(email_header_value[i])
    print("header: ")
    print(''.join(from_address_in_header))
    return ''.join(from_address_in_header)


def extract_from_address_in_payload(email_object, header_key_to_extract):
    start_point = 0
    stop_point = 0
    
    #email_payload_as_string = email_object[eml_key_to_search]
    #refactor to find "FROM address"
    email_payload_as_string = str(email_object.get_payload()[0])
    
    try:
        start_point = email_payload_as_string.index('<')
        stop_point = email_payload_as_string.index('>')
        #buggy way to handle tags    
        if (stop_point - start_point) >= 40:            
            return extract_value_in_header(email_object,"From")
    except (ValueError,OSError) as verr:        
        print(verr)

    extracted_from_address = []
    for i in range(start_point+1,stop_point):
        extracted_from_address.append(email_payload_as_string[i])    
    if '@' not in extracted_from_address:
        return extract_value_in_header(email_object,"From")
    print("payload: ")
    print(''.join(extracted_from_address))
    #bad solution to remove newline character in from address string
    result = ''.join(extracted_from_address)
    result = result.strip('\n')
    return result


def get_list_of_incoming_emails(current_eml_path):
    email_list = []
    for each_element in os.listdir(current_eml_path):
        if each_element.endswith(".eml"):
            email_list.append(each_element)
    if not email_list:
        return None
    return email_list


def get_eml_header(input_file_path):
    input_file_as_path = open(input_file_path,"r")
    return message_from_file(input_file_path)._headers


def get_value_by_key(eml_header,key_to_search):
    for key,value in eml_header:
        if key == key_to_search:
            return value
    return None


def get_email_addr_from_obfuscated_string(obfuscated_string):
    email_address = []
    start_point = obfuscated_string.index("<")+1
    stop_point = obfuscated_string.index(">")
    for i in range(start_point,stop_point):
        email_address.append(obfuscated_string[i])

    if not email_address:
        return None
    return ''.join(email_address)


def create_email_storing_folder_if_not_exists(folder_name,folder_path):
    try:
        check = os.listdir(os.path.join(folder_path,folder_name))
        if check:
            print("")
            #print("folder %s already exists"%folder_name)
    except FileNotFoundError as err:
        os.mkdir(os.path.join(folder_path,folder_name))
        print("created storing folder %s at %s"%(folder_name,os.getcwd()))


def copy_email_to_storing_folder(src,dst,email_file_name):
    if not os.path.isfile(email_file_name):
        try:
            shutil.copy2(os.path.join(src,email_file_name),os.path.join(dst,email_file_name))
        except shutil.Error as e:
            print("")
    else:
        print("already exists")


def move_copied_email_to_treasure(src,treasure_path,email_file_name,dst=None):
    create_email_storing_folder_if_not_exists(treasure_path,"")
    try:
        shutil.move(os.path.join(src,email_file_name),treasure_path)
    except shutil.Error as e:
        print("")
        #print("dup")


def get_message_content_in_email_file(main_store,email_file_name):
    email_object = message_from_file(open(os.path.join(main_store,email_file_name),"r"))
    if email_object.is_multipart():
        for each_element in email_object.walk():
            if each_element.get_content_type() == "text/plain":
                return each_element.get_payload()
    return None


def do_the_classification_job(current_eml_path,treasure_path,eml_key_to_search):
    email_list = get_list_of_incoming_emails(current_eml_path)

    if email_list is not None:
        for each_mail in email_list:
            #from_addr = extract_from_address_in_payload(get_email_object(current_eml_path,each_mail),"From")            
            from_addr = extract_value_in_header(get_email_object(current_eml_path,each_mail),"From")
            create_email_storing_folder_if_not_exists(from_addr, "mainstore")
            copy_email_to_storing_folder(current_eml_path, os.path.join("mainstore",from_addr), each_mail)
            move_copied_email_to_treasure(current_eml_path, treasure_path, each_mail)
    else:
        print("empty email list")


def get_list_of_current_dirs(current_path):
    ''' [NOT COMPLETED] 
    list dirs in current path. 
    '''
    current_dirs = []
    for each_element in os.listdir(current_path):        
            current_dirs.append(each_element)            
    return current_dirs
