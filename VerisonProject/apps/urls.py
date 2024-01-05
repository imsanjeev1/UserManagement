from django.urls import path
from . import views
urlpatterns = [
    # path("", views.login1, name="index1"),
    path('', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path("register/", views.register, name="register"),
    path("home/", views.home, name="home"),
    path("file_upload/", views.upload_csv_data, name="file_upload"),
    path("download/", views.download_file, name="download_file"),
    # path("upload_csv/", admin.upload_csv, name="upload_csv")

    # path("csv_data/", views.csv_data, name="csv_data"),
    path("hierarchy/data", views.employee_hierarchy, name="employee_hierarchy"),
    path("hierarchy/get/empdata", views.employee_hierarchy_data, name="employee_hierarchy_data"),

    ]
# from . import views
from django.contrib import admin
# admin.site.site_url = ''
admin.site.site_title = "AgreeYa"
# admin.site.site_title = "AgreeYa"
admin.site.site_header = "AgreeYa Application"
# admin.site.index_title = "AgreeYa Application333333333"
admin.autodiscover()
# admin.site.site_url = None
# admin.site.si = None
