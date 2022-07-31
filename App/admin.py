from django.contrib import admin

from .models import Profile, Subscription,Waste

admin.site.register(Profile)
admin.site.register(Waste)
admin.site.register(Subscription)
