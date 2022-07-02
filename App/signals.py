from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

def User_Profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance,name=instance.username)

post_save.connect(User_Profile,sender=User)