from django.db import models

# Create your models here.
class Email(models.Model):
    description = models.CharField(max_length=255,blank=True)
    content = models.FileField(upload_to='email/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
