from django.contrib import admin
from django.contrib.admin import widgets
from .models import Employees
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib import messages
from django.urls import path
from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class EmpResource(resources.ModelResource):
    class Meta:
        model = Employees
        import_id_fields = ('name',)
        # fields = ('name', 'title')


# Register your models here.
class FileUpload(forms.Form):
    # view_on_site = False
    # site_url = None
    select_csv_File=forms.FileField()

class EmployeeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = EmpResource

    search_fields = ['uniqueIdentifier','name','reportsTo','designation','address','organisationName','remarks']
    list_display = ['uniqueIdentifier','name','reportsTo','designation','address','organisationName','remarks','status']

    fields = ['uniqueIdentifier', 'name', 'reportsTo', 'designation', 'address', 'organisationName', 'remarks',
              'status']
    list_per_page = 10
    list_max_show_all = 6
    admin.site.site_url = "/hierarchy/data"
    # admin.site.site_url = ""

    actions = ['activate', 'deactivate']

    def activate(self, request, queryset):
        queryset.update(status=True)
        messages.success(request, "User successfully Activated.")

    def deactivate(self, request, queryset):
        queryset.update(status=False)
        messages.warning(request, "User successfully deactivated.")

admin.site.register(Employees,EmployeeAdmin)