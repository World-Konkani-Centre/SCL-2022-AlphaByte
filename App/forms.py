from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile,Waste

from PIL import Image

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
        fields = ['name','about','location','street','city','state','phone']

class ProfImageUpdateForm(ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    class Meta:
        model = Profile
        fields = ['profile_pic','x','y','width','height']
    def save(self):
        photo = super(ProfImageUpdateForm,self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')
        image = Image.open(photo.profile_pic.path)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((150, 150), Image.ANTIALIAS)
        resized_image.save(photo.profile_pic.path)
        return photo

class AddWasteForm(ModelForm):
    class Meta:
        model = Waste
        fields = ['id','company','type','weight','entry_date']

class PickUpDate(ModelForm):
    class Meta:
        model = Waste
        fields = ['employee','entry_date']

class DropdownDate(ModelForm):
    class Meta:
        model = Waste
        fields = ['employee','recycler','dropdown_date']

class PickUpDone(ModelForm):
    class Meta:
        model = Waste
        fields = ['id','pickup_done']

class DropdownDone(ModelForm):
    class Meta:
        model = Waste
        fields = ['id','dropdown_done']
