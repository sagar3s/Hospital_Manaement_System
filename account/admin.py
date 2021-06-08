from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Patient, User, Appointment,Prescription

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(Prescription)