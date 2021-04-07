from django import forms
from .models import Patient, Doctor
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PatientSignupForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('Address', 'Phone', 'gender','blood_group', 'age')

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model= User
        fields=['first_name','last_name','username','email','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorSignupForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('address','contact','department','profile_pic','gender')