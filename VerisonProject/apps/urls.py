from django.urls import path
from . import views
urlpatterns = [
    # path("", views.login1, name="index1"),
    path('', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
    path("register/", views.register, name="register"),
    path("index/", views.home, name="index"),
    path("file_upload/", views.upload_csv_data, name="file_upload"),
    path("csv_data/", views.csv_data, name="csv_data"),

    ]
# from . import views
from django.contrib import admin
admin.site.site_title = "AgreeYa Application"
admin.site.site_header = "AgreeYa Application"