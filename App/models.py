from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50,default='satviksnayak')
    about = models.TextField(blank=True)
    location = models.TextField(blank=True)
    phone = models.IntegerField(blank=True)
    def __str__(self):
        return self.name