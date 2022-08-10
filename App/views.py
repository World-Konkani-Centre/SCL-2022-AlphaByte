from datetime import datetime, timedelta
from django.utils import timezone
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import uuid

from .forms import AddWasteForm,CreateUserForm,ProfileUpdateForm,ProfImageUpdateForm,Done,SetDate
from .decorators import allowed_user, unauthenticated_user
from .models import Profile,Waste,Subscription
from .functions import chartFunc,checkWaste,grouplist

import razorpay

@unauthenticated_user
def register(request):
    form  = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            user.groups.add(request.POST.get('group'))
            if request.POST.get('group') == '3':
                subUser = Subscription(name = user)
                print(subUser)
                subUser.save()
            messages.success(request,'Account was created for '+ username)
            return redirect('login')
    context = {'form':form}
    return render(request,'App/auth/register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            if user.profile.location is None:
                return redirect('updateInfo')
            else:
                return redirect('home')
    context = {}
    return render(request,'App/auth/login.html',context)

@login_required(login_url='login')
def updateInfo(request):
    groups = grouplist(request.user)
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request,'Profile Updated!!')
            return redirect('home')
    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'groups':groups,'p_form':p_form}
    return render(request,'App/auth/register_update.html',context)

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
        img_form = ProfImageUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if p_form.is_valid() and img_form.is_valid():
            img_form.save()
            p_form.save()
            messages.success(request,'Profile Updated!!')
            return redirect('profile')
    else:
        img_form = ProfImageUpdateForm(instance=request.user.profile)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {'groups':groups,'p_form':p_form,'img_form':img_form}
    return render(request,'App/profile/profileUpdate.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Employee'])
def report(request):
    groups = grouplist(request.user)
    user = User.objects.get(username = request.user.username)
    all_wastes = Waste.objects.filter(employee = user)
    wastesP = all_wastes.filter(pickup_date = datetime.date(datetime.now()))
    W1 = Paginator(wastesP,10)
    Pwastes_today = W1.get_page(request.GET.get('page'))
    wastesD = all_wastes.filter(dropdown_date = datetime.date(datetime.now()))
    W2 = Paginator(wastesD,10)
    Dwastes_today = W2.get_page(request.GET.get('page'))
    all_wastesP = all_wastes.filter(dropdown_done = False)
    W3 = Paginator(all_wastesP,10)
    Pwastes = W3.get_page(request.GET.get('page'))
    all_wastesD = all_wastes.filter(pickup_done = True)
    W4 = Paginator(all_wastesD,10)
    Dwastes = W4.get_page(request.GET.get('page'))
    if request.method == 'POST':
        form = Done(request.POST,instance=Waste.objects.filter(id = request.POST.get('id')).first())
        if form.is_valid():
            form.save()
            return redirect('report')  
    context = {'groups':groups,'Pwastes_today':Pwastes_today,'Dwastes_today':Dwastes_today,'Pwastes':Pwastes,'Dwastes':Dwastes}
    return render(request,'App/tables/employee.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Recycler'])
def schedule(request):
    groups = grouplist(request.user)
    user = User.objects.get(username = request.user.username)
    all_wastes = Waste.objects.filter(recycler = user).order_by('dropdown_date')
    W = Paginator(all_wastes,10)
    wastes = W.get_page(request.GET.get('page'))
    context = {'groups':groups,'wastes':wastes}
    return render(request,'App/tables/recyclecomp.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Company'])
def addWaste(request):
    groups = grouplist(request.user)
    user = User.objects.get(username = request.user.username)
    all_wastes = Waste.objects.filter(company = user).order_by('-entry_date')
    W = Paginator(all_wastes,10)
    wastes = W.get_page(request.GET.get('page'))
    addWasteForm = AddWasteForm()
    uid = uuid.uuid1()
    date = str(datetime.date(datetime.now()))
    if request.method == 'POST':
        form = AddWasteForm(request.POST)
        exist = checkWaste(request.POST.get('type'),date,request.user)
        if exist is None:
            if form.is_valid():
                form.save()
                return redirect('addwaste')
        else:
            updateWaste = Waste.objects.filter(id = exist).first()
            updateWaste.weight = updateWaste.weight + int(request.POST.get('weight'))
            updateWaste.save()
            return redirect('addwaste')
    context = {'groups':groups,'addWasteForm':addWasteForm,'wastes':wastes,'uuid':uid,'date':date}
    return render(request,'App/tables/wasteprod.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Manager'])
def manager(request):
    groups = grouplist(request.user)
    all_wastes_pickup = Waste.objects.filter(pickup_done=False)
    wastes_pickup = all_wastes_pickup.filter(pickup_date=None).order_by('entry_date')
    W1 = Paginator(wastes_pickup,10)
    update_pickup = W1.get_page(request.GET.get('page'))
    W2 = Paginator(all_wastes_pickup,10)
    pickup = W2.get_page(request.GET.get('page'))
    all_wastes_dropdown = Waste.objects.filter(pickup_done=True)
    wastes_dropdown = all_wastes_dropdown.filter(dropdown_date=None).order_by('pickup_date')
    W3 = Paginator(wastes_dropdown,10)
    update_dropdown = W3.get_page(request.GET.get('page'))
    W4 = Paginator(all_wastes_dropdown,10)
    dropdown = W4.get_page(request.GET.get('page'))
    employees = User.objects.filter(groups='4')
    recyclers = User.objects.filter(groups='3')
    UWaste=[]
    date=""
    if request.method == 'POST':
        if 'pickup_date' not in request.POST:
            UWaste = Waste.objects.filter(id=request.POST.get('id')).first()
            date = str(UWaste.pickup_date)
        else:
            form = SetDate(request.POST,instance=Waste.objects.filter(id = request.POST.get('id')).first())
            if form.is_valid():
                form.save()
                return redirect('manager')
    context = {'groups':groups,'update_pickup':update_pickup,'pickup':pickup,'date':date,'update_dropdown':update_dropdown,'dropdown':dropdown,'employees':employees,'recyclers':recyclers,'Waste':UWaste}
    return render(request,'App/tables/manager.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Recycler'])
def subscriptions(request):
    groups = grouplist(request.user)
    subscription = Subscription.objects.filter(name=request.user).first()
    payment = []
    showPrem = showBasic = True
    if subscription.paid:
        if subscription.subscription_end <= timezone.now():
            subscription.paid = False
            subscription.save()
    if request.method == 'POST':
        name= request.POST.get('name')
        amount = int(request.POST.get('amount'))*100   
        if amount==2400000:
            showBasic=False
        else:
            showPrem=False 
        client = razorpay.Client(auth=('rzp_test_zdPB2yUq5SbCeW','TvzdDOGzQz7Xlj42qppCZVs6'))
        payment = client.order.create({"amount":amount,"currency":"INR","payment_capture":"1"})
        subscription.subscription_date = datetime.now()
        subscription.subscription_end = datetime.now()+ timedelta(days=365)
        subscription.subscription_id = payment['id']
        subscription.amount = amount
        subscription.save()
    if subscription.paid:
        duration=subscription.subscription_end-timezone.now()
        hours=0
        if duration.days<=0:
            seconds=duration.total_seconds()
            hours=seconds/3600
        if subscription.amount==2400000:
            showBasic=False
        else:
            showPrem=False
        context = { 'payment':payment,
                    'showBasic':showBasic,
                    'showPrem':showPrem,
                    'paid':subscription.paid,
                    'days1':duration.days%10,
                    'days2':int((duration.days/10)%10),
                    'days3':int((duration.days/100)%10),
                    'time1':int(hours%10),
                    'time2':int((hours/10)%10),
                    'date':subscription.subscription_date.date(),
                    'end':subscription.subscription_end.date(),
                    'groups':groups
                }
    else:
        context = {'payment':payment,
                   'showBasic':showBasic,
                   'showPrem':showPrem,
                   'paid':subscription.paid,
                   'groups':groups
                  }
    return render(request,'App/profile/subscriptions.html',context)
    

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Recycler'])
@csrf_exempt
def successpayment(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key,val in a.items():
            if key == 'razorpay_order_id':
                order_id = val
                break
        user = Subscription.objects.filter(name = request.user).first()
        if user.subscription_id == order_id:
            user.paid = True
            user.save()
    return render(request,"App/profile/success.html")

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Company','Recycler'])
def Charts(request):
    groups = grouplist(request.user)
    types = ['STEEL','E-WASTE','BIO-DEGRADABLE','PAPER']
    wastedata = Waste.objects.filter(company=request.user)
    data1 = chartFunc(wastedata,types)
    data = {'Steel':data1[0],'Ewaste':data1[1],'Bio':data1[2],'Paper':data1[3]}
    context = {'groups':groups,'data':data}
    return render(request,'App/profile/charts.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['admin','Company'])
def Rewards(request):
    groups = grouplist(request.user)
    context = {'groups':groups}
    return render(request,'App/profile/rewards.html',context)


def error_404(request, exception):
    return render(request, 'App/404.html')