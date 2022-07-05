from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','email']

class ProfileUpdateForm(ModelForm):
    class Meta:   
        model = Profile
        fields = ['name','about','profile_pic','location','phone']