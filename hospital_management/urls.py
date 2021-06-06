"""hospital_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from account import views
from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth.views import LoginView,LogoutView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name='home'),
    path('admin_signup/',views.signup_admin,name='admin_signup'),
    path('doctor_signup/',views.signup_doctor,name='doctor_register'),
    path('patient_signup/',views.signup_patient,name='patient_register'),
    path('login', LoginView.as_view(template_name='login.html'),name='login'),
    path('logout', LogoutView.as_view(),name='logout'),
    path('check', views.check_user_type,name='check'),
    path('admin_view', views.admin_dashboard,name="admin_dashboard"),
    path('admin_create_appointment', views.admin_create_appointment,name="admin_create_appointment"),
    path('admin_view_doctors', views.admin_view_doctors,name="admin_view_doctors"),
    path('admin_add_doctor', views.admin_add_doctor,name="admin_add_doctor"),
    path('admin_approve_doctors', views.admin_approve_doctors,name="admin_approve_doctors"),
    path('approve_doctor/<int:pk>', views.approve_doctor,name="approve_doctor"),
    path('disapprove_doctor/<int:pk>', views.disapprove_doctor,name="disapprove_doctor"),
    path('admin_update_doctor/<int:pk>', views.admin_update_doctor,name="admin_update_doctor"),
    path('admin_delete_doc/<int:pk>', views.admin_delete_doc,name="admin_delete_doc"),
    path('admin_approve_patient', views.admin_approve_patient,name="admin_approve_patient"),
    path('admin_view_patient', views.admin_view_patient,name="admin_view_patient"),
    path('admin_add_patient', views.admin_add_patient,name="admin_add_patient"),
    path('approve_patient/<int:pk>', views.approve_patient,name="approve_patient"),
    path('disapprove_patient/<int:pk>', views.disapprove_patient,name="disapprove_patient"),
    path('admin_update_patient/<int:pk>', views.admin_update_patient,name="admin_update_patient"),
    path('admin_delete_pat/<int:pk>', views.admin_delete_pat,name="admin_delete_pat"),
    path('admin_view_appointment', views.admin_view_appointment,name="admin_view_appointment"),
    path('admin_approve_appointment', views.admin_approve_appointment,name="admin_approve_appointment"),
    path('approve_appointment/<int:pk>', views.approve_appointment,name="approve_appointment"),
    path('reject_appointment/<int:pk>', views.reject_appointment,name="reject_appointment"),

    path('doctor_view', views.doctor_dashboard,name="doctor_dashboard"),
    path('doctor_view_patient', views.doctor_view_patient,name="doctor_view_patient"),
    path('doctor_view_appointment', views.doctor_view_appointment,name="doctor_view_appointment"),
    path('doctor_approve_appointment', views.doctor_approve_appointment,name="doctor_approve_appointment"),
    path('doctor_add_prescription', views.doctor_add_prescription,name="doctor_add_prescription"),
    path('doctor_manage_prescription', views.doctor_manage_prescription,name="doctor_manage_prescription"),
    path('d_delete_prescription/<int:pk>', views.d_delete_prescription,name="d_delete_prescription"),
    path('d_approve_appointment/<int:pk>', views.d_approve_appointment,name="d_approve_appointment"),
    path('d_reject_appointment/<int:pk>', views.d_reject_appointment,name="d_reject_appointment"),


    path('patient_view', views.patient_dashboard,name="patient_dashboard"),
    path('patient_view_doctors', views.patient_view_doctors,name="patient_view_doctors"),
    path('patient_view_appointment', views.patient_view_appointment,name="patient_view_appointment"),
    path('patient_create_appointment', views.patient_create_appointment,name="patient_create_appointment"),
    path('patient_view_prescription', views.patient_view_prescription,name="patient_view_prescription"),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 

