from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


from .forms import CreateUserForm
from .decorators import allowed_user, unauthenticated_user


def grouplist(user):
    groups = []
    if user.groups.exists():
        for i in range(len(user.groups.all())):
            groups.append(user.groups.all()[i].name)
    return groups

@unauthenticated_user
def register(request):
    form  = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            user.groups.add(request.POST.get('group'))
            messages.success(request,'Account was created for '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request,'App/register.html',context)

@unauthenticated_user
def loginPage(request):
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
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/home.html',context)

def Awareness(request):
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/home.html',context)

@login_required(login_url='login')
def ProfilePage(request):
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/profile.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Employee'])
def report(request):
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/employee.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Recycler'])
def schedule(request):
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/recyclecomp.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Company'])
def addWaste(request):
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/wasteprod.html',context)
