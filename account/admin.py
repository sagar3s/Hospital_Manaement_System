from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Patient, User
# Register your models here.
class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)