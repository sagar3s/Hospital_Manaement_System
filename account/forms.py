from django import forms
from .models import  Appointment, Patient , Doctor, User
from django.contrib.auth.forms import UserCreationForm

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientUserForm(forms.ModelForm):
    model=User
    fields=['f_name','l_name','username','pass']
    widgets ={
        'pass': forms.PasswordInput()
    }
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('Address', 'Phone', 'gender','blood_group', 'age')

class DoctorUserForm(forms.ModelForm):
    model=User
    fields=['f_name','l_name','username','pass']
    widgets ={
        'pass': forms.PasswordInput()
    }

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('address','contact','department','status','profile_pic','gender')