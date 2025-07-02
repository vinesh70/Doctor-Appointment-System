# api/urls.py
from django.urls import path
from api import views  # or whatever your app name is


urlpatterns = [
    # Doctor endpoints
    path('doctors/', views.DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor-detail'),
    path('doctors/<int:doctor_id>/appointments/', views.doctor_appointments, name='doctor-appointments'),
    
    # Patient endpoints
    path('patients/', views.PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('patients/<int:patient_id>/appointments/', views.patient_appointments, name='patient-appointments'),
    
    # Appointment endpoints
    path('appointments/', views.AppointmentListCreateView.as_view(), name='appointment-list-create'),
    path('appointments/<int:pk>/', views.AppointmentDetailView.as_view(), name='appointment-detail'),
    path('appointments/<int:appointment_id>/complete/', views.complete_appointment, name='complete-appointment'),
    
    # Dashboard
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]