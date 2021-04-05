from django import forms
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class Registration_Form(UserCreationForm):
    user_choice = (
        (1, 'doctor'),
        (2, 'patient'),
    )
    email = forms.EmailField()
    user_type = forms.ChoiceField(choices=user_choice, widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = [
            'first_name','last_name','username','email','password1','password2','user_type',
        ]

class PatientSignupForm(forms.ModelForm):
    class Meta:
        model = models.Patient
        fields = ('Address', 'Phone', 'gender','blood_group', 'age','status')

class DoctorSignupForm(forms.ModelForm):
    class Meta:
        model = models.Doctor
        fields = ('address','contact','department','status','profile_pic','gender')