from django.conf import settings
from . import forms,models

from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.shortcuts import render,redirect,reverse,HttpResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'index.html')
def login_page(request):
    return render(request, 'login.html')
def register(request):
    return render(request, 'register.html')
def signup_admin(request):
    if request.method=="POST":
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            admingrp=Group.objects.get_or_create(name='admin')
            admingrp[0].user_set.add(user)
            return HttpResponse("admin registered")
    else:
        form=forms.AdminSigupForm()
    return render(request,'admin_signup.html', {'form':form,})

def signup_doctor(request):

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
            return HttpResponse("Successfully Registered Now login to access Doctor Dashboard")
    else:
        form1=forms.DoctorUserForm()
        form2=forms.DoctorSignupForm()
    return render(request,'signup_doctor.html',{'form1': form1, 'form2': form2, })

def signup_patient(request):
    if request.method == "POST":
        form1=forms.PatientUserForm(request.POST)
        form2=forms.PatientSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            doc_details=form2.save(commit=False)
            doc_details.user=user
            doc_details=doc_details.save()
            doc_grp=Group.objects.get_or_create(name="patient")
            doc_grp[0].user_set.add(user)
            return HttpResponse("Successfully Registered Now login to access Patient Dashboard")
    else:
        form1=forms.PatientUserForm()
        form2=forms.PatientSignupForm()
    return render(request,'signup_patient.html',{'form1': form1, 'form2': form2, })


def logged_as_admin(user):
    return user.groups.filter(name='admin').exists()
def logged_as_doctor(user):
    return user.groups.filter(name='doctor').exists()
def logged_as_patient(user):
    return user.groups.filter(name='patient').exists()


def postlogin(request):
    if logged_as_admin(request.user):
        return redirect('admin_dashboard')
    elif logged_as_doctor(request.user):
        account_is_approved=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if account_is_approved:
            return redirect('doctor_dashboard')
        else:
            return render(request,'pending_doctor.html')
    elif logged_as_patient(request.user):
        account_is_approved=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if account_is_approved:
            return redirect('patient_dashboard')
        else:
            return render(request,'pending_patient.html')
