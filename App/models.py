from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string

from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    about = models.TextField(blank=True,null=True)
    profile_pic = models.ImageField(default='avatar.png',upload_to='Profile')
    location = models.CharField(max_length=50,blank=True,null=True)
    street = models.CharField(max_length=50,blank=True,null=True)
    city = models.CharField(max_length=30,blank=True,null=True)
    state = models.CharField(max_length=30,blank=True,null=True)
    phone = PhoneNumberField(blank=True,null=True)
    def __str__(self):
        return self.name


class Waste(models.Model):
    class Types(models.TextChoices):
        STEEL = "STEEL","Steel"
        BIODEGRADABLE = "BIO-DEGRADABLE","Bio-Degradable"
        PAPER = "PAPER","Paper"
        EWASTE = "E-WASTE","E-Waste"
    id = models.CharField(primary_key=True,default=get_random_string(length=15),max_length=15,unique=True)
    recycler = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='recycler')
    company = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='company')
    employee = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='employee')
    entry_date = models.DateField(null=True,blank=True)
    pickup_date = models.DateField(null=True,blank=True)
    dropdown_date = models.DateField(null=True,blank=True)
    weight = models.FloatField(null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    type = models.CharField(_("Types"),max_length=50,choices=Types.choices)
    pickup_done = models.BooleanField(default=False)
    dropdown_done = models.BooleanField(default=False)
    def __str__(self):
        return self.id
