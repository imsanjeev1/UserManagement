from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegisterForm
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from .models import EmployeeList
from .resources import EmployeeDataResources
from django.contrib import messages
import csv,io
from tablib import Dataset
# Create your views here.
def login1(request):
    return render(request, "login.html")

def register(request):
    if request.user.is_authenticated:
        return redirect("index")
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

def sign_in(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method =="POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect("index")
            else:
                messages.info(request,"Username OR password do not match")
                return render(request, "login.html")
        context={}
        return render(request, "login.html")
def sign_out(request):
    logout(request)
    return render(request, "login.html")

@login_required(login_url='login')
def home(request):
    return render(request, "index.html")

def upload_csv_data(request):
    import time
    # import sys
    # sys.path.append("D:\pycharm-debug")
    # import pydevd
    # pydevd.settrace('localhost', port=6086, stdoutToServer=True, stderrToServer=True)
    import pandas as pd
    if request.method == 'POST':
        customer_resources=EmployeeDataResources()
        dataset=Dataset()
        csv_file = request.FILES['upload_csv_file']
        if not csv_file.name.endswith('.csv'):
            return JsonResponse({'error': 'File is not a CSV'})

        # filename = request.FILES['data_file']
        # print(">>.", filename)
        # data_read = pd.read_csv(csv_file, delimiter=',')
        data_read = csv_file.read().decode('UTF-8')
        io_string= io.StringIO(data_read)
        next(io_string)
        for column in csv.reader(io_string,delimiter=',',quotechar="|"):
            created = EmployeesList.objects.update_or_create(
                UniqueIdentifier=column[0],
                Name=column[1],
                ReportsTo=column[2],
                Designation=column[3]

            )
        # name = data_read["Name"]
        # address = data_read["Address"]
        # phone = data_read["Phone"]
        # email = data_read["Email"]
        # column_names = list(data_read.columns)
        # Save the uploaded file to a specified location on the server
        actual_file= str(time.time())+'_'+csv_file.name
        # with open('./media/'+actual_file, 'wb+') as destination:
        # with open('./media/scrub/csv_file.csv', 'wb+') as destination:
        #     for chunk in csv_file.chunks():
        #         destination.write(chunk)
    #     return JsonResponse({'success': True, 'filename':actual_file})
    # else:
    #     return JsonResponse({'error': 'POST request required'})
    return render(request, "index.html")

def csv_data(request):
    data = EmployeeList.objects.all()
    data1 = [x for x in data]
    print("Backend Data>> ", data)
    return render(request, "csv_upload.html", {'db_data1': data})