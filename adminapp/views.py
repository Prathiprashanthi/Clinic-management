from django.shortcuts import render,redirect
from mainapp.models import*
from userapp.models import*
from adminapp.models import *
from django.contrib import messages
from django.core.paginator import Paginator
def admin_dashboard(request):
    all_patient_count =  PatientModel.objects.all().count()
    pending_patient_count = PatientModel.objects.filter(patient_status  = 'Pending').count()
    rejected_patient_count = PatientModel.objects.filter(patient_status   = 'removed').count()
    accepted_patient_count =PatientModel.objects.filter(patient_status = 'accepted').count() 
    return render(request,'admin/admin-dashboard.html',{'a' :all_patient_count, 'b' : pending_patient_count, 'c' : rejected_patient_count, 'd' : accepted_patient_count})

def admin_Pendingrequests(request):
    pending = PatientModel.objects.filter(patient_status='pending')
    paginator = Paginator(pending, 5) 
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request,'admin/admin-Pendingrequests.html', { 'user' : post})

def admin_manageclinic(request):
    all_users  = PatientModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number )
    return render(request,'admin/admin-manageclinic.html', {"allu" : all_users , 'user' : post})


def delete_user(req, id):
    user = PatientModel.objects.get(patient_id=id)
    user.delete()
    messages.warning(req, 'User was Deleted..!')
    return redirect('admin_manageclinic')

def change_status(req, id):
    user = PatientModel.objects.get(patient_id=id)
    if user.patient_status == 'Accepted':
        user.patient_status = 'Rejected'
        messages.success(req, 'Status Successfully Changed')
    else:
        user.patient_status = 'Accepted'
        messages.success(req, 'Status Successfully Changed')
    user.save()
   
    return redirect('admin_manageclinic')

def accept_user(req, id):
    status_update = PatientModel.objects.get(patient_id= id)
    status_update.patient_status = 'accepted'
    status_update.save()
    messages.success(req, 'User was accepted..!')
    return redirect('admin_Pendingrequests')

def reject_user(req, id):
    status_update2 = PatientModel.objects.get(patient_id = id)
    status_update2.patient_status  = 'removed'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('admin_Pendingrequests')

def admin_clinicdetails(request):
    pending = ClinicModel.objects.filter(clinic_status='pending')
    paginator = Paginator(pending, 5) 
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request,'admin/admin-clinicdetails.html', { 'use' : post})

def admin_manage_clinic(request):
    all_users  = ClinicModel.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number )
    return render(request,'admin/admin-manage-clinic.html', {"allu" : all_users , 'user' : post})


def clinic_delete_user(request, id):
    user = ClinicModel.objects.get(clinic_id=id)
    user.delete()
    messages.warning(request, 'User was Deleted..!')
    return redirect('admin_manage_clinic')

def change_clinic_status(req, id):
    user = ClinicModel.objects.get(clinic_id=id)
    if user.clinic_status == 'Accepted':
        user.clinic_status = 'Rejected'
        messages.success(req, 'Status Successfully Changed')
    else:
        user.clinic_status = 'Accepted'
        messages.success(req, 'Status Successfully Changed')
    user.save()
   
    return redirect('admin_manage_clinic')

def clinic_accept_user(req, id):
    status_update = ClinicModel.objects.get(clinic_id= id)
    status_update.clinic_status = 'accepted'
    status_update.save()
    messages.success(req, 'User was accepted..!')
    return redirect('admin_clinicdetails')

def clinic_reject_user(req, id):
    status_update2 = ClinicModel.objects.get(clinic_id = id)
    status_update2.clinic_status  = 'removed'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('admin_clinicdetails')

def admin_viewappointments(request):
    all_users  = Appointment.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number )
    return render(request,'admin/admin-viewappointments.html',{"allu" : all_users , 'us' : post})

def admin_pendingdoctors(request):
    pending = Doctors.objects.filter(doctor_status='pending')
    paginator = Paginator(pending, 5) 
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number)
    return render(request,'admin/admin-pendingdoctors.html', { 'doctor' : post})

def admin_alldoctors(request):
    all_users  = Doctors.objects.all()
    paginator = Paginator(all_users, 5)
    page_number = request.GET.get('page')
    post = paginator.get_page(page_number )
    return render(request,'admin/admin-alldoctors.html', {"allu" : all_users , 'user' : post})

def accept_doctor(req, id):
    status_update = Doctors.objects.get(doctor_id= id)
    status_update.doctor_status = 'accepted'
    status_update.save()
    messages.success(req, 'User was accepted..!')
    return redirect('admin_pendingdoctors')

def reject_doctor(req, id):
    status_update2 = Doctors.objects.get(doctor_id = id)
    status_update2.doctor_status  = 'removed'
    status_update2.save()
    messages.warning(req, 'User was Rejected..!')
    return redirect('admin_pendingdoctors')
def delete_doctor(req, id):
    user = Doctors.objects.get(doctor_id=id)
    user.delete()
    messages.warning(req, 'User was Deleted..!')
    return redirect('admin_alldoctors')


def doctor_change_status(req, id):
    user = Doctors.objects.get(doctor_id=id)
    if user.doctor_status == 'Accepted':
        user.doctor_status = 'Rejected'
        messages.success(req, 'Status Successfully Changed')
    else:
        user.doctor_status = 'Accepted'
        messages.success(req, 'Status Successfully Changed')
    user.save()
    return redirect('admin_alldoctors')

def admin_Feedback(request):
    feed =Feedback.objects.all()
    return render(request,'admin/admin-Feedback.html', {'back':feed})
def admin_sentimentanalysis(request):
    fee = Feedback.objects.all()
    return render(request,'admin/admin-sentimentanalysis.html', {'cat':fee})
def admin_sentimentgraph(request):
    positive = Feedback.objects.filter(Sentiment = 'positive').count()
    very_positive = Feedback.objects.filter(Sentiment = 'very positive').count()
    negative = Feedback.objects.filter(Sentiment = 'negative').count()
    very_negative = Feedback.objects.filter(Sentiment = 'very negative').count()
    neutral = Feedback.objects.filter(Sentiment= 'neutral').count()
    context ={
        'vp': very_positive, 'p':positive, 'n':negative, 'vn':very_negative, 'ne':neutral
    }
    return render(request,'admin/admin-sentimentgraph.html',context)

