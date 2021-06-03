from django.conf import settings
from . import forms,models
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, render,redirect,reverse,HttpResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def homepage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('check')
    return render(request,'index.html')
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
        form2=forms.DoctorSignupForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            doc_details=form2.save(commit=False)
            doc_details.user=user
            doc_details=doc_details.save()
            doc_grp=Group.objects.get_or_create(name="doctor")
            doc_grp[0].user_set.add(user)
            return redirect('login')
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
            pat_details=form2.save(commit=False)
            pat_details.user=user
            pat_details=pat_details.save()
            pat_grp=Group.objects.get_or_create(name="patient")
            pat_grp[0].user_set.add(user)
            return redirect('login')
    else:
        form1=forms.PatientUserForm()
        form2=forms.PatientSignupForm()
    return render(request,'signup_patient.html',{'form1': form1, 'form2': form2, })

def doctor_view_patient(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'doctor_view_patient.html',{'patients':patients})
def doctor_view_discharge_patient(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'doctor_view_discharge_patient.html',{'patients':patients})
def doctor_view_appointment(request):
    return render(request,'doctor_view_appointment.html')
def doctor_delete_appointment(request):
    return render(request,'doctor_delete_appointment.html')
def patient_view_doctors(request):
    return render(request,'patient_view_doctors.html')
def patient_view_appointment(request):
    return render(request,'patient_view_appointment.html')
def patient_add_appointment(request):
    return render(request,'patient_add_appointment.html')

def logged_as_admin(user):
    return user.groups.filter(name='admin').exists()
def logged_as_doctor(user):
    return user.groups.filter(name='doctor').exists()
def logged_as_patient(user):
    return user.groups.filter(name='patient').exists()


def check_user_type(request):
    if logged_as_admin(request.user):
        return HttpResponseRedirect('admin_view')
    elif logged_as_doctor(request.user):
        account_is_approved=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if account_is_approved:
            return HttpResponseRedirect('doctor_view')
        else:
            return render(request,'pending_doctor.html')
    elif logged_as_patient(request.user):
        account_is_approved=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if account_is_approved:
            return HttpResponseRedirect('patient_view')
        else:
            return render(request,'pending_patient.html')
    else:
        return HttpResponseRedirect('admin')
        
#COntrol Admin Dashboard
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_dashboard(request):
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    approved_doc_count=models.Doctor.objects.all().filter(status=True).count()
    pending_doc_count=models.Doctor.objects.all().filter(status=False).count()
    approved_patient_count=models.Patient.objects.all().filter(status=True).count()
    pending_patient_count=models.Patient.objects.all().filter(status=False).count()
    approved_appointment_count=models.Appointment.objects.all().filter(status=True).count()
    pending_appointment_count=models.Appointment.objects.all().filter(status=False).count()
    data={
        'doctors':doctors,
        'patients':patients,
        'no_of_approved_doctor':approved_doc_count,
        'no_of_pending_doctor':pending_doc_count,
        'no_of_approved_patient':approved_patient_count,
        'no_of_pending_patient': pending_patient_count,
        'no_of_approved_appointment':approved_appointment_count,
        'no_of_pending_appointment': pending_appointment_count,
    }
    return render(request,'admin_dashboard.html',context=data)
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_view_doctors(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'admin_view_doctors.html',{'doctors':doctors})
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_update_doctor(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    form1=forms.DoctorUserForm(instance=user)
    form2=forms.DoctorSignupForm(request.FILES,instance=doctor)
    if request.method=='POST':
        form1=forms.DoctorUserForm(request.POST,instance=user)
        form2=forms.DoctorSignupForm(request.POST,request.FILES,instance=doctor)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            doc_details=form2.save(commit=False)
            doc_details.status=True
            doc_details.save()
            return redirect('admin_view_doctor')
    return render(request,'admin_update_doctor.html',{'form1':form1,'form2':form2,})
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_update_patient(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)

    form1=forms.PatientUserForm(instance=user)
    form2=forms.PatientSignupForm(request.FILES,instance=patient)
    if request.method=='POST':
        form1=forms.PatientUserForm(request.POST,instance=user)
        form2=forms.PatientSignupForm(request.POST,request.FILES,instance=patient)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            pat_details=form2.save(commit=False)
            pat_details.status=True
            pat_details.save()
            return redirect('admin_view_patient')
    return render(request,'admin_update_patient.html',{'form1':form1,'form2':form2})
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_delete_doc(request,pk):
    doctors=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctors.user_id)
    user.delete()
    doctors.delete()
    return redirect('admin_view_doctors')
def admin_approve_doctors(request):
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'admin_approve_doctor.html',{'doctors':doctors})
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def approve_doctor(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin_approve_doctors')) 
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def disapprove_doctor(request,pk):
    doctors=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctors.user_id)
    user.delete()
    doctors.delete()
    return redirect('admin_approve_doctors')

@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_view_patient(request):
    patients=models.Patient.objects.all().filter(status=True)
    return render(request,'admin_view_patient.html',{'patients':patients}) 
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_approve_patient(request):
    patients=models.Patient.objects.all().filter(status=False)
    return render(request,'admin_approve_patient.html',{'patients':patients})
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_delete_pat(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin_view_patient')
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def approve_patient(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin_approve_patient')) 
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def disapprove_patient(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin_approve_patient')

@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_create_appointment(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin_view_appointment')
    return render(request,'admin_create_appointment.html',context=mydict)

@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_view_appointment(request):
    appointment=models.Appointment.objects.all().filter(status=True)
    return render(request,'admin_view_appointment.html',{'appointment':appointment}) 

@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_add_doctor(request):
    if request.method == "POST":
        form1=forms.DoctorUserForm(request.POST)
        form2=forms.DoctorSignupForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            doc_details=form2.save(commit=False)
            doc_details.user=user
            doc_details.status=True
            doc_details=doc_details.save()
            doc_grp=Group.objects.get_or_create(name="doctor")
            doc_grp[0].user_set.add(user)
            return redirect('admin_view_doctors')
    else:
        form1=forms.DoctorUserForm()
        form2=forms.DoctorSignupForm()
    return render(request,'admin_add_doctor.html',{'form1': form1, 'form2': form2, })

def admin_add_patient(request):
    if request.method == "POST":
        form1=forms.PatientUserForm(request.POST)
        form2=forms.PatientSignupForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            pat_details=form2.save(commit=False)
            pat_details.user=user
            pat_details.status=True
            pat_details=pat_details.save()
            pat_grp=Group.objects.get_or_create(name="patient")
            pat_grp[0].user_set.add(user)
            return redirect('admin_view_patient')
    else:
        form1=forms.PatientUserForm()
        form2=forms.PatientSignupForm()
    return render(request,'admin_add_patient.html',{'form1': form1, 'form2': form2, })

def admin_approve_appointment(request):
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'admin_approve_appointment.html',{'appointments':appointments},)

#Doctor's Section
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_dashboard(request):
    data={}
    return render(request,"doctor_dashboard.html",context=data)

@login_required(login_url='login')
@user_passes_test(logged_as_patient)
def patient_dashboard(request):
    data={}
    return render(request,"patient_dashboard.html",context=data)


