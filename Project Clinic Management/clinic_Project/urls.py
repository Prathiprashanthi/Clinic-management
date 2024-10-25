"""clinic_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views as main_views
from userapp import views as user_views
from adminapp import views as admin_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    #patient
    path('admin/', admin.site.urls),
    path('',main_views.home,name='home'),
    path('user-about',main_views.user_about,name='user_about'),
    path('user-contact',main_views.user_contact,name='user_contact'),
    path('patient-login',main_views.patient_login,name='patient_login'),
    path('user-admin',main_views.user_admin,name='user_admin'),
    path('user-register',main_views.user_register,name='user_register'),
    path('clinic-login',main_views.clinic_login,name="clinic_login"),
    path('clinic-register',main_views.clinic_register,name='clinic_register'), 
    path('patient-dashboard',main_views.patient_dashboard,name='patient_dashboard'),
    path('patient-viewdoctors',main_views.patient_viewdoctors,name='patient_viewdoctors'),
    path('patient-appointments',main_views.patient_appointments,name='patient_appointments'),
    path('patient-profile',main_views.patient_profile,name='patient_profile'),
    path('myappointments',main_views.myappointments,name='myappointments'),
    path('patient-viewprescription',main_views.patient_viewprescription,name='patient_viewprescription'),
    path('patient-feedback',main_views.patient_feedback,name='patient_feedback'),
    path('view-doctors/<int:id>/',main_views.view_doctors,name="view_doctors"),
    #path('download/', main_views.download_prescription, name='download_prescription'),
    
   # clinic
    path('clinic-dashboard',user_views.clinic_dashboard,name='clinic_dashboard'),
    path('clinic-addprescription',user_views.clinic_addprescription,name='clinic_addprescription'),
    path('clinic-allappointments',user_views.clinic_allappointments,name='clinic_allappointments'),
    path('clinic-addnewdoctor',user_views.clinic_addnewdoctor,name='clinic_addnewdoctor'),
    path('clinic-managedoctor',user_views.clinic_managedoctor,name='clinic_managedoctor'),
    path('clinic-pendingappointments',user_views.clinic_pendingappointments,name='clinic_pendingappointments'),
    path('doctor-accept-user/<int:id>',user_views.doctor_accept_user, name = 'doctor_accept_user'),
    path('delete/<int:id>/',user_views.doctor_delete_user, name='doctor_delete_user'),
    path('doctor-reject-user/<int:id>',user_views.doctor_reject_user, name = 'doctor_reject_user'),
    path('doctor-change-status/<int:id>',user_views.doctor_status, name ='doctor_status'),
    path('accept-appointment/<int:id>', user_views.accept_appointment, name = 'accept_appointment'),
    path('delete-appointment/<int:id>', user_views.delete_appointment, name = 'delete_appointment'),
    path('reject-appointment/<int:id>', user_views.reject_appointment, name = 'reject_appointment'),
    path('appointment-change-status/<int:id>',user_views.appointment_status, name ='appointment_status'),
   #admin
    path('admin-dashboard',admin_views.admin_dashboard,name='admin_dashboard'),
    path('admin-alldoctors',admin_views.admin_alldoctors,name='admin_alldoctors'),
    path('admin-clinicdetails',admin_views.admin_clinicdetails,name='admin_clinicdetails'),
    path('admin-manageclinicdetails',admin_views.admin_manage_clinic,name='admin_manage_clinic'),
    
    path('change-clinic-status/<int:id>/',admin_views.change_clinic_status,name="change_clinic_status"),
   
    
    
    path('admin-manageclinic',admin_views.admin_manageclinic,name='admin_manageclinic'),
    path('admin-pendingdoctors',admin_views.admin_pendingdoctors,name='admin_pendingdoctors'),
    path('admin-Pendingrequests',admin_views.admin_Pendingrequests,name='admin_Pendingrequests'),
    path('accept-user/<int:id>', admin_views.accept_user, name = 'accept_user'),
    path('delete-user/<int:id>', admin_views.delete_user, name = 'delete_user'),
    path('reject-user/<int:id>', admin_views.reject_user, name = 'reject'), 
    
    path('accept-doctor/<int:id>', admin_views.accept_doctor, name = 'accept_doctor'),
    path('delete-doctor/<int:id>', admin_views.delete_doctor, name = 'delete_doctor'),
    path('reject-doctor/<int:id>', admin_views.reject_doctor, name = 'reject_doctor'), 
    path('doctor-change-status/<int:id>',admin_views.doctor_change_status, name ='doctor_change_status'),
    
      
    path('clinic-accept-user/<int:id>', admin_views.clinic_accept_user, name = 'clinic_accept_user'),
    path('clinic-delete-user/<int:id>', admin_views.clinic_delete_user, name = 'clinic_delete_user'),
    path('clinic-reject-user/<int:id>', admin_views.clinic_reject_user, name = 'clinic_reject_user'),
    path('admin-change-status/<int:id>',admin_views.change_status, name ='change_status'),
    path('admin-Feedback',admin_views.admin_Feedback,name='admin_Feedback'),
    path('admin-sentimentanalysis',admin_views.admin_sentimentanalysis,name='admin_sentimentanalysis'),
    path('admin-sentimentgraph',admin_views.admin_sentimentgraph,name='admin_sentimentgraph'),
    path('admin-viewappointments',admin_views.admin_viewappointments,name='admin_viewappointments'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
