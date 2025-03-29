from django.db import models

class UploadedFile(models.Model):
    file=models.FileField(upload_to='invoices/')
    extracted_text=models.TextField(blank= True)

    def __str__(self):
        return f"Invoice {self.id}"
    
