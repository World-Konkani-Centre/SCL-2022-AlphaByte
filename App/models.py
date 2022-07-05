from distutils.command.upload import upload
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=50)
    about = models.TextField(blank=True,null=True)
    profile_pic = models.ImageField(default='avatar.png',upload_to='Profile')
    location = models.TextField(blank=True,null=True)
    phone = models.IntegerField(blank=True,null=True)
    def __str__(self):
        return self.name
    def save(self):
        super().save()
        img = Image.open(self.profile_pic.path)
        if img.width>150 :
            output_size = (150,150)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)