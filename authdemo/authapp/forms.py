from django import forms
# from .models import CustomUserModel
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserChangeForm,UserCreationForm,UserChangeForm

class SignUpForm(UserCreationForm):
    # username = forms.CharField(max_length=30)
    email = forms.EmailField(required = True)
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']


class ProfileChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True)
    email = forms.EmailField(required = True)
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']

class RoleForm(forms.ModelForm):
    class Meta:
        model = Group 
        fields = ['name']

class CreateStaffEmployeeForm(UserCreationForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    class Meta:
        model= User
        fields = ['username','email','first_name','last_name']


class EditEmployeeForm(UserChangeForm):
    role = forms.ModelChoiceField(queryset=Group.objects.all(),required=False)
    password = None

    class Meta:
        model = User
        fields = ['email','first_name','last_name']