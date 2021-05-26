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
    path('doctor_view', views.doctor_dashboard,name="doctor_dashboard"),
    path('patient_view', views.patient_dashboard,name="patient_dashboard"),
    path('admin_add_appointment', views.admin_add_appointment,name="admin_add_appointment"),
    path('admin_view_doctors', views.admin_view_doctors,name="admin_view_doctors"),
    path('admin_approve_doctor', views.admin_approve_doctor,name="admin_approve_doctor"),
    path('admin_approve_patient', views.admin_approve_patient,name="admin_approve_patient"),
    path('admin_view_patient', views.admin_view_patient,name="admin_view_patient"),
    path('admin_discharge_patient', views.admin_discharge_patient,name="admin_discharge_patient"),
    path('admin_view_appointment', views.admin_view_appointment,name="admin_view_appointment"),
    path('admin_approve_appointment', views.admin_approve_appointment,name="admin_approve_appointment"),
    path('doctor_view_patient', views.doctor_view_patient,name="doctor_view_patient"),
    path('doctor_view_discharge_patient', views.doctor_view_discharge_patient,name="doctor_view_discharge_patient"),
    path('doctor_view_appointment', views.doctor_view_appointment,name="doctor_view_appointment"),
    path('doctor_delete_appointment', views.doctor_delete_appointment,name="doctor_delete_appointment"),
    path('patient_view_doctors', views.patient_view_doctors,name="patient_view_doctors"),
    path('patient_view_appointment', views.patient_view_appointment,name="patient_view_appointment"),
    path('patient_add_appointment', views.patient_add_appointment,name="patient_add_appointment"),
]
