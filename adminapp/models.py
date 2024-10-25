from django.db import models
from userapp.models import Doctors,Feedback
from mainapp.models import PatientModel
# Create your models here.
class ClinicModel(models.Model):
    CLINIC_TYPE_CHOICES = [
        ('hospital', 'Hospital'),
        ('clinic', 'Clinic'),
        ('diagnostic_center', 'Diagnostic Center'),
    ]

    clinic_id = models.AutoField(primary_key=True)
    clinic_name = models.CharField(max_length=100)
    clinic_type = models.CharField(max_length=50, choices=CLINIC_TYPE_CHOICES)
    contact = models.CharField(max_length=20)
    email = models.EmailField()
    clinic_password = models.CharField(max_length=100,null=True)
    clinic_city=models.TextField(null=True)
    address = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    clinic_status=models.CharField(help_text='clinic_status',max_length=50,null=True,default='pending')
    photo = models.ImageField(upload_to='images/') 
    license = models.FileField(upload_to='media/')
   
    class Meta:
        db_table = 'clinic_details'
        
# Create your models here.
class Appointment(models.Model):
    SERVICE_CHOICES = [
        ('dentist', 'Dentist'),
        ('doctor', 'Doctor'),
        ('physical-therapy', 'Physical Therapy'),
    ]
    
    CLINIC_CHOICES = [
        ('in-clinic', 'In-clinic'),
        ('virtual', 'Virtual'),
    ]
    
    service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    date = models.DateField()
    time = models.TimeField()
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    clinic = models.CharField(max_length=20, choices=CLINIC_CHOICES)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    appointment_status = models.CharField(max_length=50, help_text='Appointment status', null=True, default='pending')
    patient=models.ForeignKey(PatientModel, on_delete=models.CASCADE,null=True)
    appointed_doctor = models.CharField(max_length=20,null=True)
    class Meta:
        db_table = 'appointment_details'



class Prescription(models.Model):
    patient=models.ForeignKey(PatientModel, on_delete=models.CASCADE,null=True)
    prescription_file = models.FileField(upload_to='prescriptions/', blank=True, null=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Ensure only one instance of Prescription exists
        if Prescription.objects.exists():
            self.pk = Prescription.objects.first().pk
        super(Prescription, self).save(*args, **kwargs)

    class Meta:
        db_table = 'prescription_details'