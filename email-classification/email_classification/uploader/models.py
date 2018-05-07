import os
import hashlib

from django.db import models
from django.db.utils import IntegrityError
from django.core.files.storage import FileSystemStorage

# Create your models here.

class EmailFileSystemStorage(FileSystemStorage):
    def _save(self,name,content):
        if self.exists(name):
            print("\nduplicated eml file name\n")
            return name
        return super(EmailFileSystemStorage,self)._save(name,content)


class Email(models.Model):
    '''
        7/5: adding attr: current_location, number_of_attachment
    '''
    #id = models.CharField(primary_key=True,max_length=100, unique = True)
    md5sum = models.CharField(max_length = 100, primary_key = True)
    description = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.FileField(storage=EmailFileSystemStorage(location='temp-email-storage'))
    ######################
    current_location = models.URLField(max_length=200,blank=True)
    number_of_attachment = models.SmallIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.pk:
            md5 = hashlib.md5()
            for chunk in self.content.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(Email,self).save(*args,**kwargs)
        

    
            
