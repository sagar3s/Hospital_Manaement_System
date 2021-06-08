
from django.db.models import fields
import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class appointment_filter(django_filters.FilterSet):
    patient=django_filters.ModelChoiceFilter(queryset=Patient.objects.all().filter(status=True))
    doctor=django_filters.ModelChoiceFilter(queryset=Doctor.objects.all().filter(status=True))
    class Meta:
	    model = Appointment
	    fields = '__all__'
	    exclude = ['appt_time_to', 'appt_time_from','description','status']
class pending_appointment_filter(django_filters.FilterSet):
    patient=django_filters.ModelChoiceFilter(queryset=Patient.objects.all().filter(status=True))
    doctor=django_filters.ModelChoiceFilter(queryset=Doctor.objects.all().filter(status=True))
    class Meta:
	    model = Appointment
	    fields = '__all__'
	    exclude = ['appt_time_to', 'appt_time_from','description','status']
class doctor_filter(django_filters.FilterSet):
    class Meta:
	    model = Doctor
	    fields = ['department']
class doc_view_appt(django_filters.FilterSet):
    patient=django_filters.ModelChoiceFilter(queryset=Patient.objects.all().filter(status=True))
    class Meta:
	    model = Appointment
	    fields = '__all__'
	    exclude = ['doctor','appt_time_to', 'appt_time_from','description','status']

class presc_filt(django_filters.FilterSet):
	doctor=django_filters.ModelChoiceFilter(queryset=Doctor.objects.all().filter(status=True))
	symptom=django_filters.CharFilter(field_name='symptom',lookup_expr='icontains')
	class Meta:
	    model = Prescription
	    fields = '__all__'
	    exclude = ['patient','prescription']
class pat_view_appt(django_filters.FilterSet):
    doctor=django_filters.ModelChoiceFilter(queryset=Doctor.objects.all().filter(status=True))
    class Meta:
	    model = Appointment
	    fields = '__all__'
	    exclude = ['patient','appt_time_to', 'appt_time_from','description',]

