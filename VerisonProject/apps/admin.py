from django.contrib import admin

from import_export.admin import ImportExportModelAdmin
from .models import EmployeeList
from django import forms
from django.urls import path
from django.shortcuts import render
# import import

# @admin.register(ImportExportModelAdmin)
class FileUpload(forms.Form):
    csv_upload=forms.FileField()


@admin.register(EmployeeList)
class csvfiledataAdmin(ImportExportModelAdmin):
    list_display = ('UniqueIdentifier','Name','ReportsTo','Designation')

    def get_urls(self):
        urls=super().get_urls()
        new_urls=[path('upload-csv/',self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):
        return render(request,"csv_upload.html")


#Register your models here.
