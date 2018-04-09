from django import forms
from .models import Email

class EmailUploadForm(forms.ModelForm):
    file_field = forms.FileField(widget = forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Email
        fields = ('description',)
