from django.shortcuts import render,redirect
from adminapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
import os
# Create your views here.
def clinic_dashboard(request):
    all_patient_count =  Doctors.objects.all().count()
    pending_patient_count = Doctors.objects.filter(doctor_status  = 'Pending').count()
    rejected_patient_count = Doctors.objects.filter(doctor_status   = 'removed').count()
    accepted_patient_count =Doctors.objects.filter(doctor_status = 'accepted').count() 
    all_doctors  = Doctors.objects.all()
    paginator = Paginator(all_doctors, 5)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number )
    return render(request,'user/clinic-dashboard.html',{'a' :all_patient_count, 'b' : pending_patient_count, 'c' : rejected_patient_count, 'd' : accepted_patient_count,"allu" : all_doctors , 'user' : post})
def clinic_addnewdoctor(request):
    if request.method == 'POST':
        doctor_name = request.POST.get("doctor")
        doctor_exp=request.POST.get("experience")
        doctor_spec=request.POST.get("speciality")
        doctor_avilday=request.POST.get("day")
        doctor_date=request.POST.get("date")
        doctor_time=request.POST.get("timings")
        doctor_fee = request.POST.get("consultation_fee")
        doctor_img=request.FILES.get("file_upload")
        print(doctor_name,doctor_exp,doctor_spec,doctor_avilday,doctor_time,doctor_fee,doctor_img, doctor_date, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        
        doctors = Doctors.objects.create(
            full_name=doctor_name,
            experience=doctor_exp,
            speciality=doctor_spec,
            day_available=doctor_avilday,
            timings_available=doctor_time,
            consultation_fee=doctor_fee,
            doctor_image=doctor_img,
            date= doctor_date
        )
       
        doctors.save()
    return render(request,'user/clinic-addnewdoctor.html')
def clinic_managedoctor(request):
    doctors = Doctors.objects.all()
    return render(request,'user/clinic-managedoctor.html', {'doctors': doctors})

def doctor_delete_user(req, id):
    user = Doctors.objects.get(doctor_id=id)
    user.delete()
    messages.warning(req, 'User was Deleted..!')
    return redirect('clinic_managedoctor')

def doctor_status(req, id):
    user = Doctors.objects.get(doctor_id=id)
    if user.doctor_status == 'accept':
        user.doctor_status = 'reject'
        messages.success(req, 'Status Successfully Changed to Unavialble')
    else:
        user.doctor_status = 'accept'
        messages.success(req, 'Status Successfully Changed to avialble')
    user.save()
    return redirect('clinic_managedoctor')


def doctor_accept_user(req, id):
    status_update = Doctors.objects.get(doctor_id= id)
    status_update.doctor_status = 'accepted'
    status_update.save()
    messages.success(req, 'User was accepted..!')
    return redirect('clinic_managedoctor')

def doctor_reject_user(req, id):
    status_update2 = Doctors.objects.get(doctor_id = id)
    status_update2.doctor_status  = 'Pending'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('clinic_managedoctor')




def clinic_pendingappointments(request):
    app =Appointment.objects.all()
    return render(request,'user/clinic-pendingappointments.html', {'app': app})


def delete_appointment(req, id):
    user = Appointment.objects.get(id=id)
    user.delete()
    messages.warning(req, 'User was Deleted..!')
    return redirect('clinic_allappointments')

def appointment_status(req, id):
    user = Appointment.objects.get(id=id)
    if user.appointment_status == 'accepted':
        user.appointment_status = 'rejected'
        messages.success(req, 'Status Successfully Changed to Unavialble')
    else:
        user.appointment_status = 'accepted'
        messages.success(req, 'Status Successfully Changed to avialble')
    user.save()
    return redirect('clinic_allappointments')

from django.core.mail import send_mail
def accept_appointment(req, id):
    appointment = Appointment.objects.get(id=id)
    appointment.appointment_status = 'accepted'
    appointment.save()
    appointment.appointment_status = 'accepted'
    appointment.save()

    # Retrieve the associated patient's email
    email = appointment.email

    # Send email to the patient
    subject = 'Appointment Confirmation'
    message = f'Your appointment with {appointment.clinic} has been accepted. Date: {appointment.date}, Time: {appointment.time}.'
    from_email = 'your@example.com'  # Update with your email address
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    # Display success message
    messages.success(req, 'Appointment accepted successfully. Email notification sent to the patient.')

    messages.success(req, 'User was accepted..!')
    return redirect('clinic_allappointments')

def reject_appointment(req, id):
    status_update2 = Appointment.objects.get(id = id)
    status_update2.appointment_status  = 'pending'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('clinic_allappointments')

def clinic_allappointments(request):
    all_appointments  = Appointment.objects.all()
    paginator = Paginator(all_appointments, 5)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request,'user/clinic-allappointments.html', {"allu" : all_appointments, 'user' : post,})
from django.conf import settings


def clinic_addprescription(request):
    if request.method == 'POST':
        prescription_file = request.FILES.get('prescription')
        user_id = request.POST.get('user_id') 
        
        if prescription_file and user_id:
            try:
                # Get existing Prescription record if it exists
                prescription = Prescription.objects.first()
            except Prescription.DoesNotExist:
                prescription = None
            
            # If there's an existing prescription, update it; otherwise, create a new one
            if prescription:
                prescription.prescription_file = prescription_file
                prescription.save()
            else:
                patient = Appointment.objects.get(id=user_id).patient
                
                upload_dir = os.path.join(settings.MEDIA_ROOT, 'prescriptions')
                os.makedirs(upload_dir, exist_ok=True)
                with open(os.path.join(upload_dir, prescription_file.name), 'wb+') as destination:
                    for chunk in prescription_file.chunks():
                        destination.write(chunk)
                
                prescription = Prescription.objects.create(patient=patient, prescription_file='prescriptions/' + prescription_file.name)
            
            return redirect('clinic_addprescription')
    
    users = Appointment.objects.all()
    paginator = Paginator(users, 5)
    page_number = request.GET.get('page')
    users_paginated = paginator.get_page(page_number)
    return render(request, 'user/clinic-addprescription.html', {"allu": users, 'user': users_paginated})