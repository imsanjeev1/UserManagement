from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import EmployeeList
from django import forms
from django.urls import path
from django.shortcuts import render
import csv,io
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

class FileUpload(forms.Form):
    csv_upload=forms.FileField()


class csvfiledataAdmin(admin.ModelAdmin):
    list_display = ('UniqueIdentifier','Name','ReportsTo','Designation')

    def get_urls(self):
        urls=super().get_urls()
        new_urls=[path('upload-csv/',self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):
        if request.method=="POST":
            print("Action >>>POST")
            csv_file=request.FILES["csv_upload"]
            if not csv_file.name.endswith('.csv'):
                messages.warning(request,'File type not supported')
                return HttpResponseRedirect(request.path_info)
            data_read = csv_file.read().decode('UTF-8')
            # file_data =data_read.split("\n")
            io_string = io.StringIO(data_read)
            next(io_string)
            for column in csv.reader(io_string,delimiter=',',quotechar="|"):
                created = EmployeeList.objects.update_or_create(
                    UniqueIdentifier=column[0],
                    Name=column[1],
                    ReportsTo=column[2],
                    Designation=column[3]

                )
            url=reverse('admin:index')
            return HttpResponseRedirect(url)

        form = FileUpload()
        upload_form = {'form':form}
        return render(request,"admin/csv_upload.html",upload_form)


admin.site.register(EmployeeList,csvfiledataAdmin)
#Register your models here.
