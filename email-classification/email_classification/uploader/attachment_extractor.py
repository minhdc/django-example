import os
import base64
import patoolib


def has_attachment(email_header):
    for k,v in email_header:        
        if k == "Content-Type":
            if 'multipart/mixed' in v:
                return True
    return False


def get_email_subject(email_header):
    for k,v in email_header:
        if k == "Subject":
            print("subject:",v)
            return v


def get_multiple_attachment(email_object):
    payload = email_object.get_payload()
    list_attachment = []
    #need to count the number of attachments then update in to attachment_number in database field
                #
                #
                #
    for part in email_object.walk():
        if 'application' in part.get_content_type():
            list_attachment.append(part)
    return list_attachment


def write_multiple_attachment(list_attachment,path,email_name):
    '''
        copy attachment to the folder which name is corresponding to the file
    '''
    #need to count the number of attachments then update in to attachment_number in database field
                #
                #
                #
    for attachment in list_attachment:
        file_name = attachment.get_filename()
        data = base64.b64decode(attachment.get_payload())
        dest = os.path.join(path,email_name)
        if not os.path.isdir(dest):
            os.mkdir(dest)
        try:
            with open(os.path.join(dest,file_name),"wb") as attch:
                attch.write(data)
        except Error as e:
            print(e)
            pass
    print("successfuly copy attachment to store")
        
