from django import forms
from .models import UploadedFile

class UploadFileForm(forms.ModelForm):
    file =forms.FileField(label="Upload the extraction file: ",required=True)
    class Meta:
        model = UploadedFile
        fields =['file']