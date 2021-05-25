from django.db import models
from django.contrib.auth.models import User
import datetime

GENDER_CHOICE = (
    (1, 'Female'),
    (2, 'Male'),
    (3, 'Others'),
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
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICE, default=3)
    age = models.IntegerField(blank=True, default=None, null=True)
    blood_group = models.PositiveSmallIntegerField(
        choices=BLOOD_GROUPS, default=7)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)


class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profilepic/Doctor/',null=True,blank=True)
    contact = models.CharField(max_length=20,null=True)
    gender = models.PositiveSmallIntegerField(
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
        return "{}".format(self.user.first_name)
        


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)
