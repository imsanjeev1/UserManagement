from import_export import resources
from .models import EmployeeList

class EmployeeDataResources(resources.ModelResource):
    class Meta:
        model = EmployeeList
