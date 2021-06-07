from django import forms
from . import models
from .models import Patient, Doctor, Appointment,Prescription
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
        fields = ('Address', 'Phone', 'gender','blood_group', 'age','profile_pic')

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

class admin_appointment(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (admin_appointment,self ).__init__(*args,**kwargs) 
        self.fields['patient'].queryset = Patient.objects.filter(status=True)
        self.fields['doctor'].queryset = Doctor.objects.filter(status=True)
    class Meta:
        model=models.Appointment
        fields='__all__'

class patient_appointment(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (patient_appointment,self ).__init__(*args,**kwargs) 
        self.fields['doctor'].queryset = Doctor.objects.filter(status=True)
    class Meta:
        model=models.Appointment
        fields=['doctor','description','status','appt_day','appt_time_from','appt_time_to']
class PrescriptionForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (PrescriptionForm,self ).__init__(*args,**kwargs) 
        self.fields['patient'].queryset = Patient.objects.filter(status=True)
    class Meta:
        model = Prescription
        fields = ['patient','symptom','prescription']



