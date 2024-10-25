from django.shortcuts import render,redirect
from django.contrib import messages
from mainapp.models import *
from adminapp.models import *
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from userapp.models import *
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth import login
from django.utils import timezone
import pytz
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your views here.

def home(request):
    return render(request,'main/index.html')
def user_about(request):
    return render(request,'main/about.html')
def user_contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        city = request.POST.get('city')
        message = request.POST.get('message')
        print(name,email,city,message, 'uuuuuuuuuuuuuuuuuuuuuuuuuuuuu')
        PatientModel.objects.create(patient_name=name,patient_email=email,Message=message,patient_city=city)
        messages.success(request, 'Your message has been submitted successfully.')
        return redirect('user_contact')
    return render(request,'main/contact.html')
def patient_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = PatientModel.objects.get(patient_email=email)
            if user.patient_password == password:
                if user.patient_status == 'accepted': 
                    request.session['patient_id'] = user.patient_id
                    messages.success(request, 'Successfully logged in')
                    return redirect('patient_dashboard')
                elif user.patient_status == 'pending':
                    messages.warning(request, 'Your request is pending approval. Please wait for acceptance.')
                elif user.patient_status == 'declined':
                    messages.error(request, 'Your request has been declined.')
            else:
                messages.warning(request, 'Invalid email or password.')
        except PatientModel.DoesNotExist:
            messages.warning(request, 'Invalid email or password.')
    return render(request, 'main/patient-login.html')

def user_admin(request):
    admin_name = 'admin@123'
    admin_pwd = 'admin'
    if request.method == 'POST':
        admin_n = request.POST.get('adminName')
        admin_p = request.POST.get('adminPwd')
        if (admin_n == admin_name and admin_p == admin_pwd):
            messages.success(request, 'You are logged in..')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'You are trying to loging with wrong details..')
            return redirect('user_admin')
    return render(request,'main/admin.html')

def user_register(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        age = request.POST.get('age')
        dob_str = request.POST.get("date")
        email = request.POST.get("email")
        password = request.POST.get("password")
        contact = request.POST.get("contact")
        city = request.POST.get("city")
        image = request.FILES.get("image")

        try:
            # Converting the date string to the YYYY-MM-DD format
            dob = datetime.strptime(dob_str, '%m/%d/%Y').strftime('%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Invalid date format. Please use MM/DD/YYYY format.')
            return redirect('user_register')

        print(name, age, email, password, contact, image, city, dob)
        try:
            # Saving the user with the converted date string
            user = PatientModel.objects.create(
                patient_name=name,
                patient_dob=dob,
                patient_email=email,
                patient_password=password,
                patient_contact=contact,
                patient_city=city,
                patient_image=image,
                patient_age=age
            )
            messages.success(request, 'Successfully registered')
            return redirect('patient_login')
        except ValidationError as e:
            messages.error(request, e.message_dict)
            return redirect('user_register')

    return render(request, 'main/patient-register.html')
def clinic_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = ClinicModel.objects.get(email=email)
            if user.clinic_password == password:
                request.session['clinic_id'] = user.clinic_id
                if user.clinic_status == 'accepted': 
                    messages.success(request, 'Successfully logged in')
                    return redirect('clinic_dashboard')
                elif user.clinic_status == 'pending':
                    messages.warning(request, 'Your request is pending approval. Please wait for acceptance.')
                elif user.clinic_status == 'declined':
                    messages.error(request, 'Your request has been declined.')
            else:
                messages.warning(request, 'Invalid email or password.')
        except PatientModel.DoesNotExist:
            messages.warning(request, 'Invalid email or password.')
    return render(request,'main/cliniclogin.html')
def clinic_register(request):   
    if request.method == 'POST':
        clinic_name = request.POST.get('clinic_name')
        clinic_type = request.POST.get('clinic_type')
        contact = request.POST.get('contact')
        email = request.POST.get('email')
        password = request.POST.get('password')
        city = request.POST.get('city')
        address = request.POST.get('address')
        location = request.POST.get('location')
        photo = request.FILES.get('photo')
        license = request.FILES.get('license')
        
        # Perform any necessary validation
        
        # Assuming you have a Clinic model defined, you can create a new instance and save it
        new_clinic = ClinicModel.objects.create(
            clinic_name=clinic_name,
            clinic_type=clinic_type,
            contact=contact,
            email=email,
            address=address,
            location=location,
            photo=photo,
            license=license,
            clinic_password=password,
            clinic_city=city
        )
        new_clinic.save()
        if new_clinic:
            messages.success(request, 'Successfully registered')
            return redirect('clinic_login')
        else:
            messages.error(request, 'Invalid registration')
            return redirect('clinic_register')
    return render(request,'main/clinicregister.html')

def patient_dashboard(request):
    patients = PatientModel.objects.all().count()
    print(patients)
    user_id = request.session["patient_id"]
    user = PatientModel.objects.get(patient_id = user_id)
    if user.Last_Login_Time is None:
        IST = pytz.timezone('Asia/Kolkata')
        current_time_ist = datetime.now(IST).time()
        user.Last_Login_Time = current_time_ist
        user.save()
    return render(request,'main/patient-dashboard.html', {' patients_count' :  patients, 'la' : user})
def patient_viewdoctors(request):
    doctors = Doctors.objects.all()
    return render(request, 'main/patient-viewdoctors.html', {'doctors': doctors})


def view_doctors(request,id):
    doctors = Doctors.objects.filter(pk=id)
    return render(request,'main/viewdoctors.html', {'doctors': doctors})

def patient_appointments(request):
    id = request.session.get('patient_id')
    user = PatientModel.objects.get(pk=id)
    doctors = Doctors.objects.values_list('full_name', flat=True)
    patients =Appointment.objects.all().count()
    last =Doctors.objects.all()
    print(patients)
    if request.method == 'POST':
        appointment_doctor= request.POST.get('doctor')
        appointment_service = request.POST.get('service')
        appointment_date = request.POST.get('date')
        appointment_time = request.POST.get('time')
        patient_name = request.POST.get('name')
        patient_email = request.POST.get('email')
        patient_phone = request.POST.get('phone')
        appointment_clinic = request.POST.get('clinic')
        appointment_fee = request.POST.get('fee') 
        try:
            appointments = Appointment.objects.create(
                service=appointment_service,
                date=appointment_date,
                time=appointment_time,
                name=patient_name,
                email=patient_email,
                phone=patient_phone,
                clinic=appointment_clinic,
                fee=appointment_fee,
                patient = user,
                appointed_doctor=appointment_doctor,
                
            )
            appointments.save()
            messages.success(request, 'Successfully registered')
            return redirect('myappointments')
        except Exception as e:
            # Print error message for debugging
            print("Error:", e)
            messages.error(request, 'Failed to register appointment')
            return redirect('patient_appointments')
    return render(request, 'main/patient-appointments.html', {'doctors': doctors,' patients_count' :  patients,'last':last})
from datetime import datetime
def patient_profile(request):
    user_id = request.session["patient_id"]
    user = PatientModel.objects.get(patient_id = user_id)
    if request.method == 'POST':
        patient_name = request.POST.get('firstname')
        patient_age = request.POST.get('age')
        patient_phone = request.POST.get('phone')
        patient_password = request.POST.get('password')
        patient_email = request.POST.get('email')
        patient_dob = request.POST.get("date")
        try:
            # Parse the date string into a datetime object
            patient_dob = datetime.strptime(patient_dob, '%m/%d/%Y')
            # Convert the datetime object to the desired format
            patient_dob_formatted = patient_dob.strftime('%Y-%m-%d')
        except ValueError:
            pass
        patient_city =request.POST.get("city")
        
        user.patient_name = patient_name
        user.patient_age = patient_age
        user.patient_city = patient_city
        user.patient_contact = patient_phone
        user.patient_email=patient_email
        user.patient_password=patient_password
        user.patient_dob=patient_dob
       

        if len(request.FILES) != 0:
            image = request.FILES['pic']
            user.patient_image = image
            user.patient_name = patient_name
            user.patient_age = patient_age
            user.patient_city = patient_city 
            user.patient_contact= patient_phone
            user.patient_email=patient_email
            user.patient_password=patient_password
            user.patient_dob=patient_dob
            user.save()
            messages.success(request, 'Updated SUccessfully...!')
        else:
            user.patient_name = patient_name
            user.patient_age = patient_age
            user.save()
            messages.success(request, 'Updated SUccessfully...!')
            
    context = {"i":user}
    return render(request,'main/patient-profile.html',context)


def myappointments(request):
    user_id = request.session.get("patient_id")
    user = PatientModel.objects.get(pk=user_id)
    doc = Appointment.objects.filter(patient=user)
    return render(request,'main/myappointments.html', {'doc': doc})

import os
from django.conf import settings

def patient_viewprescription(request):
    user_id = request.session.get("patient_id")
    user = PatientModel.objects.get(pk=user_id)
    prescriptions = Prescription.objects.filter(patient=user)
    appointments = Appointment.objects.filter(patient=user)
    return render(request, 'main/patient-viewprescription.html', {'doc': appointments, 'prescriptions': prescriptions})



def patient_feedback(request):
    id=request.session["patient_id"]
    uusser=PatientModel.objects.get(patient_id=id)
    if request.method == "POST":
        rating=request.POST.get("rating")
        review=request.POST.get("feedback")
        # print(sentiment)        
        # print(rating,feed)
        sid=SentimentIntensityAnalyzer()
        score=sid.polarity_scores(review)
        sentiment=None
        if score['compound']>0 and score['compound']<=0.5:
            sentiment='positive'
        elif score['compound']>=0.5:
            sentiment='very positive'
        elif score['compound']<-0.5:
            sentiment='very negative'
        elif score['compound']<0 and score['compound']>=-0.5:
            sentiment='negative'
        else :
            sentiment='neutral'
        Feedback.objects.create(Rating=rating, Review=review,Sentiment=sentiment, Reviewer=uusser)
        messages.success(request,'Feedback recorded')
        return redirect('patient_feedback')
    return render(request,'main/patient-feedback.html')

