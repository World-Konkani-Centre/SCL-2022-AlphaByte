from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'App/home.html')

def report(request):
    return render(request,'App/employee.html')

def schedule(request):
    return render(request,'App/recyclecomp.html')

def addWaste(request):
    return render(request,'App/wasteprod.html')

def loginPage(request):

    return render(request,'App/login.html')

def register(request):
    
    return render(request,'App/register.html')
