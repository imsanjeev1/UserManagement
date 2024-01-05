"""VerisonProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.views.i18n import JavaScriptCatalog
from django.urls import path,include
from django.contrib import admin

# from django import *
from apps import views
urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path("hierarchy/data", views.employee_hierarchy),
    path("hierarchy/get/empdata", views.employee_hierarchy_data, name="employee_hierarchy_data"),
    path('', admin.site.urls, name='login'),
    # path('admin/', admin.site.urls),

]

from django.contrib import admin
admin.site.site_url = "/hierarchy/data"
admin.site.index_title = 'AgreeYa Application'
admin.site.site_title = "AgreeYa"
admin.site.site_header = "AgreeYa Application"

admin.autodiscover()
