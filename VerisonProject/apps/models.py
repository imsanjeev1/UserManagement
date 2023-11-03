from django.db import models

# Create your models here.
class EmployeeList(models.Model):
    UniqueIdentifier=models.CharField(max_length=200)
    Name=models.CharField(max_length=200)
    ReportsTo=models.CharField(max_length=200)
    Designation=models.CharField(max_length=200)