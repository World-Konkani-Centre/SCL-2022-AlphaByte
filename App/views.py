from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


from .forms import CreateUserForm


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form  = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,'Account was created for '+ user)
                return redirect('login')
        context = {'form':form}
        return render(request,'App/register.html',context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
        context = {}
        return render(request,'App/login.html',context)

def logOutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request,'App/home.html')

def Awareness(request):
    return render(request,'App/home.html')

@login_required(login_url='login')
def ProfilePage(request):
    return render(request,'App/home.html')

@login_required(login_url='login')
def report(request):
    return render(request,'App/employee.html')

@login_required(login_url='login')
def schedule(request):
    return render(request,'App/recyclecomp.html')

@login_required(login_url='login')
def addWaste(request):
    return render(request,'App/wasteprod.html')
