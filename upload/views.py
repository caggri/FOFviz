from django.shortcuts import render, HttpResponse
from .forms import FileForm
from upload.functions import handle_uploaded_file

# Create your views here.

def upload_page(request):
    if request.method == 'POST':  
        file_form = FileForm(request.POST, request.FILES)  
        if file_form.is_valid():  
            data_type = file_form.cleaned_data.get("TYPE")
            print(data_type)
            handle_uploaded_file(request.FILES['file'], data_type)  
            return HttpResponse("File uploaded successfuly")  
    else:  
        file_form = FileForm()  
        return render(request,"upload/index.html",{'form':file_form})  


def success_page():
    pass