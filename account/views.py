from django.conf import settings
from . import forms,models

from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,reverse

from django.core.mail import send_mail
from django.http import HttpResponseRedirect
# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')
def register(request):
    return render(request, 'register.html')
def signup_admin(request):
    form=forms.AdminSigupForm()
    if request.method=="POST":
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            admingrp=Group.objects.get_or_create(name='admin')
            admingrp[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'admin_signup.html', {'form':form,})

def signup_doctor(request):
    form1=forms.DoctorUserForm()
    form2=forms.DoctorSignupForm()
    doctor_form={
        'form1':form1,
        'form2':form2
    }
    if request.method == "POST":
        form1=forms.DoctorUserForm(request.POST)
        form2=forms.DoctorSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            doc_details=form2.save(commit=False)
            doc_details.user=user
            doc_details=doc_details.save()
            doc_grp=Group.objects.get_or_create(name="doctor")
            doc_grp[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'signup_doctor.html',context=doctor_form)

def signup_patient(request):
    form1=forms.PatientUserForm()
    form2=forms.PatientSignupForm()
    patient_form={
        'form1':form1,
        'form2':form2
    }
    if request.method == "POST":
        form1=forms.PatientUserForm(request.POST)
        form2=forms.PatientSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            pat_details=form2.save(commit=False)
            pat_details.user=user
            pat_details=pat_details.save()
            pat_grp=Group.objects.get_or_create(name="patient")
            pat_grp[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'signup_patient.html',context=patient_form)

def is_admin(user):
    return user.groups.filter(name='admin').exists()
def is_doctor(user):
    return user.groups.filter(name='doctor').exists()
def is_patient(user):
    return user.groups.filter(name='patient').exists()