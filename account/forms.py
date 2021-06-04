from django import forms
from . import models
from .models import Patient, Doctor, Appointment
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

class AppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Select Doctor Name", to_field_name="user_id")
    patientId=forms.ModelChoiceField(queryset=models.Patient.objects.all().filter(status=True),empty_label="Select a patient", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status','appt_day']


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Select Doctor Name", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status','appt_day']



