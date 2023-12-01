from django.contrib import admin
from django.contrib.admin import widgets
from .models import Employees
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import messages
from django.urls import path
from django.shortcuts import render
from django import forms
class EmpResource(resources.ModelResource):
    class Meta:
        model = Employees
        import_id_fields = ('name',)
        # fields = ('name', 'title')


# Register your models here.
class FileUpload(forms.Form):
    view_on_site = False
    site_url = None
    select_csv_File=forms.FileField()

class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EmpResource

    search_fields = ['uniqueIdentifier','name','reportsTo','designation','address','organisationName','remarks']
    list_display = ['uniqueIdentifier','name','reportsTo','designation','address','organisationName','remarks','status']

    fields = ['uniqueIdentifier', 'name', 'reportsTo', 'designation', 'address', 'organisationName', 'remarks',
              'status']
    list_per_page = 10
    list_max_show_all = 6

    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(status=True)
        messages.success(request, "User successfully Activated.")

    def deactivate(self, request, queryset):
        queryset.update(status=False)
        messages.warning(request, "User successfully deactivated.")

    def get_urls(self):
        urls=super().get_urls()
        # print("GET URLS>>>",urls)
        new_urls=[path('upload-csv/',self.upload_csv),]
        return new_urls + urls

    def upload_csv(self,request):
        form = FileUpload()
        upload_form = {'form': form}
        return render(request, "admin/csv_upload.html",upload_form)
    #

admin.site.register(Employees,EmployeeAdmin)
# class Media:
#     js = (
#         '//ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js',  # jquery
#         # 'js/admin.js',  # project static folder
#     )
