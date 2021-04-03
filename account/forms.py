from django import forms
from .models import  Appointment, Patient , Doctor, Prescription,User,Invoice
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('Address', 'Phone', 'gender', 'case_paper','records','blood_group', 'age')

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ('Address', 'Phone', 'gender', 'Department')