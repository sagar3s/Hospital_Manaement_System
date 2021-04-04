from django.db import models
from django.contrib.auth.models import User
import datetime
DEPARTMENT= (
    (1, 'Eye Care'),
    (2, 'Skin Care'),
    (3, 'Surgery'),
    (4, 'Physical Therapy'),
    (5, 'Dental'),
    (6, 'General')
)
GENDER_CHOICE = (
    (1, 'Female'),
    (2, 'Male'),
    (3, 'Others'),
)
BLOOD_GROUPS = (
    (1, 'A+'),
    (2, 'A-'),
    (3, 'B+'),
    (4, 'B-'),
    (5, 'AB+'),
    (6, 'AB-'),
    (7, 'O+'),
    (8, 'O-'),
)
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profilepic/Doctor/',null=True,blank=True)
    contact = models.CharField(max_length=20,null=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICE, default=3)
    address = models.CharField(max_length=40)
    department= models.CharField(max_length=50,choices=DEPARTMENT,default='6')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Address = models.CharField(max_length=100, blank=True, null=True)
    profile_pic= models.ImageField(upload_to='profilepic/patient',null=True,blank=True)
    Phone = models.CharField(max_length=100, blank=True, null=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICE, default=3)
    age = models.IntegerField(blank=True, default=None, null=True)
    blood_group = models.PositiveSmallIntegerField(
        choices=BLOOD_GROUPS, default=7)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"
class Appointment:
    patient=models.ForeignKey(Patient, null=True, on_delete=models.CASCADE)
    Doctor=models.ForeignKey(Doctor, null=True, on_delete=models.CASCADE)
    appt_date=models.DateField(("Date"),default=datetime.date.today)
    symptoms=models.CharField(max_length=100, null=True)
    status=models.BooleanField(default=False)


