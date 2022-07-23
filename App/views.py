from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User


from .forms import AddWasteForm, CreateUserForm,UserUpdateForm,ProfileUpdateForm,ProfImageUpdateForm
from .decorators import allowed_user, unauthenticated_user
from .models import Profile,Waste


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
    return render(request,'App/awareness.html',context)

@login_required(login_url='login')
def ProfilePage(request):
    groups = grouplist(request.user)
    if request.method == 'POST':
        # u_form = UserUpdateForm(request.POST, instance=request.user)
        img_form = ProfImageUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid() and img_form.is_valid():
            # u_form.save()
            img_form.save()
            p_form.save()
            messages.success(request,'Profile Updated!!')
            return redirect('profile')
    else:
        # u_form = UserUpdateForm(instance=request.user)
        img_form = ProfImageUpdateForm(instance=request.user.profile)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'groups':groups,'p_form':p_form,'img_form':img_form}
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
    user = User.objects.get(username = request.user.username)
    wastes = Waste.objects.filter(company = user)
    addWasteForm = AddWasteForm()
    if request.method == 'POST':
        form = AddWasteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addwaste')
    context = {'groups':groups,'addWasteForm':addWasteForm,'wastes':wastes}
    return render(request,'App/wasteprod.html',context)
