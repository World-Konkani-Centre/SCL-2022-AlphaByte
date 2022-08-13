from .models import Waste
from django.contrib.auth.models import Group,User



types = ['STEEL','E-WASTE','BIO-DEGRADABLE','PAPER']

def chartFunc(wastedata):
    data=[[],[],[],[]]
    for i in range(0,4):
        for j in range(0,12):
            data[i].append(0)
    for waste in wastedata:
        wdate = str(waste.entry_date)
        if waste.type == types[0]:
            for i in range(0,10):
                j = str(i)
                if wdate[5]=='0' and wdate[6]==j:
                    data[0][i]+=int(waste.weight)
                elif wdate[5]=='1' and wdate[6]== j:
                    data[0][10+i]+=int(waste.weight)
        elif waste.type == types[1]:
            for i in range(0,10):
                j = str(i)
                if wdate[5]=='0' and wdate[6]==j:
                    data[1][i]=data[1][i]+int(waste.weight)
                elif wdate[5]=='1' and wdate[6]==j:
                    data[1][10+i]=data[1][10+i]+int(waste.weight)
        elif waste.type == types[2]:
            for i in range(0,10):
                j = str(i)
                if wdate[5]=='0' and wdate[6]==j:
                    data[2][i]=data[2][i]+int(waste.weight)
                elif wdate[5]=='1' and wdate[6]==j:
                    data[2][10+i]=data[2][10+i]+int(waste.weight)
        else:
            for i in range(0,10):
                j = str(i)
                if wdate[5]=='0' and wdate[6]==j:
                    data[3][i]=data[3][i]+int(waste.weight)
                elif wdate[5]=='1' and wdate[6]==j:
                    data[3][10+i]=data[3][10+i]+int(waste.weight)
    return data

def grouplist(user):
    groups = []
    if user.groups.exists():
        for i in range(len(user.groups.all())):
            groups.append(user.groups.all()[i].name)
    return groups

def checkWaste(type,date,user):
    user = Waste.objects.filter(company = user)
    dateSort = user.filter(entry_date=date)
    if dateSort is not None:
        typeSort = dateSort.filter(type = type).first()
        if typeSort is not None:
            return typeSort.id
    return None

def checkRewards(user):
    data = [0,0,0,0]
    if user.groups.all()[1].name == 'Recycler':
        all_wastes = Waste.objects.filter(recycler=user,dropdown_done=True)
    elif user.groups.all()[1].name == 'Company':
        all_wastes = Waste.objects.filter(company=user,pickup_done=True)
    for waste in all_wastes:
        if waste.type == types[0]:
            data[0] += int(waste.weight)
        elif waste.type == types[1]:
            data[1] += int(waste.weight)
        elif waste.type == types[2]:
            data[2] += int(waste.weight)
        else:
            data[3] += int(waste.weight)
    disdata = [0,0,0,0]
    preReward = 0
    for i in range(4):
        disdata[i] = data[i]%100
        preReward += int(data[i]/100)
    dicts = {'data':disdata,'preReward':preReward}
    return dicts