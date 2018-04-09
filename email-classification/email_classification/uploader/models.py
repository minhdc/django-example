from django.db import models
from django.core.files.storage import FileSystemStorage

# Create your models here.
class Email(models.Model):
    description = models.CharField(max_length=255,blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.FileField(storage=FileSystemStorage(location='temp-email-storage'))
