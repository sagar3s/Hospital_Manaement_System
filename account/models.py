from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models.deletion import SET_NULL

from django.http import request

GENDER_CHOICE = (
    ('Female', 'Female'),
    ('Male', 'Male'),
    ('Others', 'Others'),
)

DEPARTMENT= (
    ('Eye Care', 'Eye Care'),
    ('Skin Care', 'Skin Care'),
    ('Surgery', 'Surgery'),
    ('Physical Therapy', 'Physical Therapy'),
    ('Dental', 'Dental'),
    ('General', 'General'),
    ('Cardiology', 'Cardiology'),
)

BLOOD_GROUPS = (
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB+'),
    ('AB-', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-'),
)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=150, blank=True, null=True)
    profile_pic= models.ImageField(upload_to='profilepic/patient',null=True,blank=True)
    Phone = models.CharField(max_length=150, blank=True, null=True)
    gender = models.CharField(
        max_length=50,
        choices=GENDER_CHOICE, default=3)
    age = models.IntegerField(blank=True, default=None, null=True)
    blood_group = models.CharField(
        max_length=50,
        choices=BLOOD_GROUPS, default='A+')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" "+self.user.last_name


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profilepic/Doctor/',null=True,blank=True)
    contact = models.CharField(max_length=20,null=True)
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICE, default=3)
    address = models.CharField(max_length=40)
    department= models.CharField(max_length=50,choices=DEPARTMENT,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "Dr. {} {} ({})".format(self.user.first_name,self.user.last_name,self.department)

class Appointment(models.Model):
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,default="")
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,default="")
    appt_day=models.DateField(null=True)
    appt_time_from=models.TimeField(null=True)
    appt_time_to=models.TimeField(null=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return "Patient-{} Symptom-{}".format(self.patient, self.description)

    
class Prescription(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    symptom=models.CharField(max_length=40,null=True)
    date = models.DateField(auto_now_add=True)
    prescription = models.TextField(default='')
    class Meta:
        ordering = ("-id",)

    def __str__(self):
        return "Treated By-{} Patient-{}".format(self.doctor, self.patient)
