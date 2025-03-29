import pandas as pd
from tabula import read_pdf
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .models import UploadedFile
import os

def upload_file(request):
    data = None  # Store extracted data
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_obj = form.save()
            pdf_path = file_obj.file.path
            
            # Extract tables using tabula
            tables = read_pdf(pdf_path, pages="all", multiple_tables=True)
            if tables:
                df = pd.concat(tables, ignore_index=True)  # Combine tables
                request.session['data'] = df.to_dict()  # Save in session
            
            return redirect('display_data')

    else:
        form = UploadFileForm()
    
    return render(request, 'invoice_upload.html', {'form': form})

def display_data(request):
    data_dict = request.session.get('data')
    if not data_dict:
        return redirect('upload_file')

    df = pd.DataFrame.from_dict(data_dict)
    return render(request, 'invoice_result.html', {'data': df.to_html(classes='table table-bordered')})

def download_excel(request):
    data_dict = request.session.get('data')
    if not data_dict:
        return redirect('upload_file')

    df = pd.DataFrame.from_dict(data_dict)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="extracted_data.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Extracted Data')

    return response