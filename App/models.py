from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    about = models.TextField(blank=True,null=True)
    profile_pic = models.ImageField(null=True,blank=True)
    location = models.TextField(blank=True,null=True)
    phone = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name