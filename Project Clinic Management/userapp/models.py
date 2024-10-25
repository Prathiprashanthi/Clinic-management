from django.db import models
from mainapp.models import PatientModel

# Create your models here.
class Feedback(models.Model):
    Feed_id = models.AutoField(primary_key=True)
    Rating=models.CharField(max_length=100,null=True)
    Review=models.CharField(max_length=225,null=True)
    Sentiment=models.CharField(max_length=100,null=True)
    Reviewer=models.ForeignKey(PatientModel, on_delete=models.CASCADE,null=True)
    datetime=models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'feedback_details'
        
class Doctors(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=100)
    experience = models.CharField(max_length=10)
    speciality = models.CharField(max_length=50)
    day_available = models.CharField(max_length=50)
    timings_available = models.CharField(max_length=50)
    doctor_status=models.CharField(help_text='doctor_status',max_length=50,null=True,default='pending')
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    doctor_image = models.ImageField(upload_to='doctor/images')
    date = models.DateField(auto_now_add=True) 
    class Meta:
        db_table = 'doctors_details'

