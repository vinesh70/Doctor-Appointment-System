from django.db import models
from django.core.validators import RegexValidator

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doctors'
        ordering = ['name']

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"


class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=15,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number.')]
    )
    date_of_birth = models.DateField()
    address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patients'
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    appointment_datetime = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['-appointment_datetime']
        unique_together = ['doctor', 'appointment_datetime']

    def __str__(self):
        return f"{self.patient.name} with {self.doctor.name} on {self.appointment_datetime}"

    def clean(self):
        from django.core.exceptions import ValidationError
        from django.utils import timezone
        
        # Check if appointment is in the future
        if self.appointment_datetime <= timezone.now():
            raise ValidationError('Appointment must be scheduled for a future date and time.')
        
        # Check for conflicting appointments
        conflicting_appointments = Appointment.objects.filter(
            doctor=self.doctor,
            appointment_datetime=self.appointment_datetime,
            status='scheduled'
        ).exclude(pk=self.pk)
        
        if conflicting_appointments.exists():
            raise ValidationError('Doctor already has an appointment at this time.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)