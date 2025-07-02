
# appointments/admin.py
from django.contrib import admin
from appointments.models import Doctor, Patient, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'phone', 'email', 'created_at']
    list_filter = ['specialization', 'created_at']
    search_fields = ['name', 'specialization', 'email']
    ordering = ['name']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'date_of_birth', 'age', 'created_at']
    list_filter = ['date_of_birth', 'created_at']
    search_fields = ['name', 'email', 'phone']
    ordering = ['name']

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_datetime', 'status', 'created_at']
    list_filter = ['status', 'appointment_datetime', 'doctor__specialization']
    search_fields = ['patient__name', 'doctor__name']
    ordering = ['-appointment_datetime']
    date_hierarchy = 'appointment_datetime'