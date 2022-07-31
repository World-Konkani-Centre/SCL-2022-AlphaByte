from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

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
    id = models.CharField(primary_key=True,unique=True,max_length=40)
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

class Subscription(models.Model):
    name = models.ForeignKey(User,on_delete=models.CASCADE,primary_key=True,unique=True)
    subscription_id = models.CharField(max_length=100,null=True,blank=True)
    paid = models.BooleanField(default=False)
    subscription_date = models.DateTimeField(blank=True,null=True)
    subscription_ends = models.DateTimeField(blank=True,null=True)
    amount = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name.username