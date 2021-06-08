from typing_extensions import Concatenate
from django.conf import settings
from django.db.models.aggregates import Count
from . import forms,models
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.shortcuts import get_list_or_404, render,redirect,reverse,HttpResponse
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .filters import appointment_filter,pending_appointment_filter,doctor_filter,doc_view_appt,presc_filt,pat_view_appt

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
        form2=forms.DoctorSignupForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            doc_details=form2.save(commit=False)
            doc_details.user=user
            doc_details=doc_details.save()
            doc_grp=Group.objects.get_or_create(name="doctor")
            doc_grp[0].user_set.add(user)
            messages.success(request,"Successfully Registered the account please login to access your dashboard")
            return redirect('login')
    else:
        form1=forms.DoctorUserForm()
        form2=forms.DoctorSignupForm()
    return render(request,'signup_doctor.html',{'form1': form1, 'form2': form2, })

def signup_patient(request):
    if request.method == "POST":
        form1=forms.PatientUserForm(request.POST)
        form2=forms.PatientSignupForm(request.POST,request.FILES)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            pat_details=form2.save(commit=False)
            pat_details.user=user
            pat_details=pat_details.save()
            pat_grp=Group.objects.get_or_create(name="patient")
            pat_grp[0].user_set.add(user)
            messages.success(request,"Successfully Registered the account please login to access your dashboard")
            return redirect('login')
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


def check_user_type(request):
    if logged_as_admin(request.user):
        return HttpResponseRedirect('admin_view')
    elif logged_as_doctor(request.user):
        account_is_approved=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if account_is_approved:
            return redirect('doctor_dashboard')
        else:
            return render(request,'pending.html')
    elif logged_as_patient(request.user):
        account_is_approved=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if account_is_approved:
            return redirect('patient_dashboard')
        else:
            return render(request,'pending.html')
    else:
        return HttpResponseRedirect('admin')
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_view_patient(request):
    doc_id=models.Doctor.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(id=doc_id.id)
    presc=models.Prescription.objects.all().filter(doctor_id=doc_id.id)
    pat_id=[]
    for a in presc:
        pat_id.append(a.patient_id)
    patint_id=set(pat_id)
    p_id=list(patint_id)
    patients=models.Patient.objects.all().filter(id__in=p_id)

    return render(request,'doctor_view_patient.html',{'patients':patients,'doctor':doctor})

#COntrol Admin Dashboard
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_dashboard(request):
    doctors=models.Doctor.objects.all().order_by('-id')[:4]
    patients=models.Patient.objects.all().order_by('-id')[:4]
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
    doctor_filt=doctor_filter(request.GET,queryset=doctors)
    doctors=doctor_filt.qs
    return render(request,'admin_view_doctors.html',{'doctors':doctors,'doctor_filt':doctor_filt})
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_update_doctor(request,pk):
    
    docid=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=docid.user_id)
    form1=forms.DoctorUserForm(instance=user)
    doctor=models.Doctor.objects.get(id=pk)
    form2=forms.DoctorSignupForm(request.FILES,instance=doctor)
    print(form1)
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
            return redirect('admin_view_doctors')
    return render(request,'admin_update_doctor.html',{'form1':form1,'form2':form2,'doctor':doctor},)
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
    return render(request,'admin_update_patient.html',{'form1':form1,'form2':form2,'patient':patient},)
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
    doctor_filt=doctor_filter(request.GET,queryset=doctors)
    doctors=doctor_filt.qs
    return render(request,'admin_approve_doctor.html',{'doctors':doctors,'doctor_filt':doctor_filt},)
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
    appt_form=forms.admin_appointment()
    mydict={'appt_form':appt_form,}
    if request.method=='POST':
        appt_form=forms.admin_appointment(request.POST)
        if appt_form.is_valid():
            appointment_data=appt_form.save(commit=False)
            appointment_data.status=True
            appointment_data.save()
        return redirect('admin_view_appointment')
    return render(request,'admin_create_appointment.html',context=mydict)

@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_view_appointment(request):
    appointment=models.Appointment.objects.all().filter(status=True)
    appt_filter=appointment_filter(request.GET,queryset=appointment)
    appointment=appt_filter.qs
    return render(request,'admin_view_appointment.html',{'appointment':appointment,'appt_filter':appt_filter,}) 

@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_add_doctor(request):
    if request.method == "POST":
        form1=forms.DoctorUserForm(request.POST)
        form2=forms.DoctorSignupForm(request.POST, request.FILES)
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
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
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
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def admin_approve_appointment(request):
    appointments=models.Appointment.objects.all().filter(status=False)
    appt_filter=pending_appointment_filter(request.GET,queryset=appointments)
    appointments=appt_filter.qs
    return render(request,'admin_approve_appointment.html',{'appointments':appointments,'appt_filter':appt_filter},)
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def approve_appointment(request,pk):
    appt=models.Appointment.objects.get(id=pk)
    appt.status=True
    appt.save()
    return redirect('admin_approve_appointment')
@login_required(login_url='login')
@user_passes_test(logged_as_admin)
def reject_appointment(request,pk):
    appt=models.Appointment.objects.get(id=pk)
    appt.delete()
    return redirect('admin_approve_appointment')

#Doctor's Section
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_dashboard(request):
    doc_id=models.Doctor.objects.get(user_id=request.user.id)
    total_docs = len(set(models.Appointment.objects.values_list('patient_id').filter(doctor_id=doc_id.id, status=True)))
    pending_appointment_no=models.Appointment.objects.all().filter(doctor_id=doc_id.id,status=False).count()
    total_treated = len(set(models.Prescription.objects.values_list('patient_id').filter(doctor_id=doc_id.id)))
    doctor=models.Doctor.objects.get(id=doc_id.id)
    appointment=models.Appointment.objects.all().filter(doctor_id=doc_id.id)
    data={
        'total': total_docs,
        'pending_appointment_no':pending_appointment_no,
        'total_treated':total_treated,
        'doctor':doctor,
        'appt':appointment,
    }
    return render(request,"doctor_dashboard.html",context=data)
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_view_appointment(request):
    doc_id=models.Doctor.objects.get(user_id=request.user.id)
    apptdoctor=models.Appointment.objects.all().filter(doctor_id=doc_id.id,status=True)
    appt_filt=doc_view_appt(request.GET,queryset=apptdoctor)
    apptdoctor=appt_filt.qs
    doctor=models.Doctor.objects.get(id=doc_id.id)
    data={
         
         'apptdoctor':apptdoctor,
         'doctor':doctor,
         'appt_filt':appt_filt
    }
    return render(request,'doctor_view_appointment.html',context=data)
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_approve_appointment(request):
    doc_id=models.Doctor.objects.get(user_id=request.user.id)
    apptdoctor=models.Appointment.objects.all().filter(doctor_id=doc_id.id,status=False)
    doctor=models.Doctor.objects.get(id=doc_id.id)
    data={
         
         'apptdoctor':apptdoctor,
         'doctor':doctor,
    }
    return render(request,'doctor_approve_appointment.html',context=data)

@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def d_approve_appointment(request,pk):
    appt=models.Appointment.objects.get(id=pk)
    appt.status=True
    appt.save()
    return redirect('doctor_view_appointment')
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def d_reject_appointment(request,pk):
    appt=models.Appointment.objects.get(id=pk)
    appt.delete()
    return redirect('doctor_view_appointment')
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_add_prescription(request):
    doc_id=models.Doctor.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(id=doc_id.id)
    if request.method=='POST':
        form1=forms.PrescriptionForm(request.POST)
        doc=models.Doctor.objects.get(user_id=request.user.id)
        if form1.is_valid():
            pat_pres=form1.save(commit=False)
            pat_pres.doctor=doc
            pat_pres.save()
            return redirect('doctor_manage_prescription')
    else:
        form1=forms.PrescriptionForm()
    return render(request,'doctor_add_prescription.html',{'form1':form1,'doctor':doctor},)

    
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def doctor_manage_prescription(request):
    docid=models.Doctor.objects.get(user_id=request.user.id)
    precs=models.Prescription.objects.all().filter(doctor_id=docid.id)
    doctor=models.Doctor.objects.get(id=docid.id)
    data={
        'presc':precs,
        'doctor':doctor,

    }
    return render(request,'doctor_manage_prescription.html',context=data)
@login_required(login_url='login')
@user_passes_test(logged_as_doctor)
def d_delete_prescription(request,pk):
    presc=models.Prescription.objects.get(id=pk)
    presc.delete()
    return redirect('doctor_manage_prescription')

@login_required(login_url='login')
@user_passes_test(logged_as_patient)
def patient_dashboard(request):
    pat_id=models.Patient.objects.get(user_id=request.user.id)
    appt_no=models.Appointment.objects.all().filter(patient_id=pat_id.id).count()
    recent_appointment=models.Appointment.objects.all().filter(patient_id=pat_id.id,status=True)[:4]
    total_docs = len(set(models.Prescription.objects.values_list('doctor_id').filter(patient_id=pat_id.id)))
    appt_pending_no=models.Appointment.objects.all().filter(patient_id=pat_id.id, status=False).count()
    patient=models.Patient.objects.get(id=pat_id.id)
    
    data={
        'appt_no':appt_no,
        'appt_approved_no':total_docs,
        'appt_pending_no':appt_pending_no,
        'recent_appointment':recent_appointment,
        'patient':patient,
    }
    return render(request,"patient_dashboard.html",context=data)

@login_required(login_url='login')
@user_passes_test(logged_as_patient)
def patient_view_doctors(request):
    doctor=models.Doctor.objects.all().filter(status=True)
    pat_id=models.Patient.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pat_id.id)
    doctor_filt=doctor_filter(request.GET,queryset=doctor)
    doctor=doctor_filt.qs
    data={
        'doctor':doctor,
        'patient':patient,
        'doctor_filt':doctor_filt
    }
    return render(request,'patient_view_doctors.html',context=data)
@login_required(login_url='login')
@user_passes_test(logged_as_patient)
def patient_create_appointment(request):
    appt_form=forms.patient_appointment()
    pat_data=models.Patient.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=pat_data.id)
    data={'appt_form':appt_form,'patient':patient,}
    if request.method=='POST':
        pat_data=models.Patient.objects.get(user_id=request.user.id)
        appt_form=forms.patient_appointment(request.POST)
        patient=models.Patient.objects.get(id=pat_data.id)
        if appt_form.is_valid():
            appointment_data=appt_form.save(commit=False)
            appointment_data.status=False
            appointment_data.patient=pat_data
            appointment_data.save()
            print(appointment_data)
        return redirect('patient_view_appointment')
    return render(request,'patient_add_appointment.html',context=data)
@login_required(login_url='login')
@user_passes_test(logged_as_patient)
def patient_view_appointment(request):
    patid=models.Patient.objects.get(user_id=request.user.id)
    patient=models.Patient.objects.get(id=patid.id)
    appt=models.Appointment.objects.all().filter(patient_id=patid.id)
    pat_appt=pat_view_appt(request.GET,queryset=appt)
    appt=pat_appt.qs

    return render(request,'patient_view_appointment.html',{'appointment':appt,'patient':patient,'pat_view_appt':pat_view_appt})
@login_required(login_url='login')
@user_passes_test(logged_as_patient)
def patient_view_prescription(request):
    patID=models.Patient.objects.get(user_id=request.user.id)
    presc_pat=models.Prescription.objects.all().filter(patient_id=patID.id)
    patient=models.Patient.objects.get(id=patID.id)
    presc=presc_filt(request.GET,queryset=presc_pat)
    presc_pat=presc.qs
    data={
        'presc_pat':presc_pat,
        'patient':patient,
        'presc_filt':presc_filt,
    }
    return render(request,'patient_view_prescription.html',context=data)


