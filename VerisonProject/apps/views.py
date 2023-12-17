from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import Employees
from .resources import csvfiledataResources
from django.contrib import messages
import csv,io
from tablib import Dataset
# Create your views here.
def login1(request):
    return render(request, "login.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("home   ")
    else:
        if request.method == 'GET':
            form = RegisterForm()
            return render(request, "register.html", { 'form': form})
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                messages.success(request, 'You have successfully singed up.')
                # login(request, user)
                return HttpResponseRedirect("/register")
            else:
                return render(request, 'register.html', {'form': form})
@login_required(login_url='login')
def sign_in(request):
    if request.user.is_authenticated:
        return redirect("employee_hierarchy")
    else:
        if request.method =="POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            # if username or password is "":
            #     messages.warning(request, "Username OR password should not be blank")
            #     return redirect("login")
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("home")
            else:
                messages.warning(request,"Username OR password do not match")
                return render(request, "login.html")
        context={}
        return render(request, "login.html")
def sign_out(request):
    logout(request)
    # return render(request, "login.html")
    return redirect("login")

@login_required(login_url='login')
def home(request):
    data = Employees.objects.all()
    return render(request, "home.html", {'db_data': data,'page_type': "Employee List"})

def upload_csv_data(request):
    import time
    if request.method == 'POST':
        customer_resources=csvfiledataResources()
        dataset=Dataset()
        csv_file = request.FILES['upload_csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.warning(request,'File is not a CSV')
            return HttpResponseRedirect("/file_upload")
            # return render(request,"file_upload.html")
            # return JsonResponse({'error': 'File is not a CSV'})
        data_read = csv_file.read().decode('UTF-8')
        io_string= io.StringIO(data_read)
        next(io_string)
        for column in csv.reader(io_string,delimiter=',',quotechar="|"):
            created = Employees.objects.update_or_create(
                uniqueIdentifier=column[0],
                name=column[1],
                reportsTo=column[2],
                designation=column[3],
                address=column[4],
                organisationName=column[5],
                remarks=column[6]

            )
    return render(request, "file_upload.html",{'page_type':"File Upload"})
    # return HttpResponseRedirect("/file_upload",{'page_type':"File Upload"})

def csv_data(request):
    data = Employees.objects.all()
    return render(request, "home.html", {'db_data': data})

def download_file(request):
    filename ="testfile.csv"
    import time
    data = Employees.objects.all()
    write_file = './media/' + filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment'; filename=write_file

    writer = csv.writer(response)
    writer.writerow(
        ['UniqueIdentifier', 'Name', 'Designation', 'ReportsTo'])

    empdata = Employees.objects.all().values_list('UniqueIdentifier', 'Name', 'Designation', 'ReportsTo')
    for info in empdata:
        writer.writerow(info)

    return JsonResponse({'success': True})

def employee_hierarchy(request):
    return render(request, "emp_hierarchy.html")

def employee_hierarchy_data(request):
    data = get_employees()

    return JsonResponse({'success': True, 'data': data})

def get_employees():
    parent = Employees.objects.filter(reportsTo='').first()
    parent_data = {"name": parent.name, "title": parent.designation}
    parent_data['children'] = get_child(parent, parent_data)
    return parent_data


def get_child(parent, result):
    children = []
    childs = Employees.objects.filter(reportsTo=parent.name)
    for child in childs:
        d_child = {"name": child.name, "title": child.designation, "children": get_child(child, result)}
        children.append(d_child)
    return children