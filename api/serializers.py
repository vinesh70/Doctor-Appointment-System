from rest_framework import serializers
from appointments.models import Doctor, Patient, Appointment
from django.utils import timezone


class DoctorSerializer(serializers.ModelSerializer):
    appointment_count = serializers.SerializerMethodField()

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'phone', 'email', 'appointment_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_appointment_count(self, obj):
        return obj.appointments.filter(status='scheduled').count()

    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        if Doctor.objects.filter(email=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value


class PatientSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField()
    appointment_count = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = ['id', 'name', 'email', 'phone', 'date_of_birth', 'age', 'address', 'appointment_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'age', 'created_at', 'updated_at']

    def get_appointment_count(self, obj):
        return obj.appointments.filter(status='scheduled').count()

    def validate_email(self, value):
        instance = getattr(self, 'instance', None)
        if Patient.objects.filter(email=value).exclude(pk=instance.pk if instance else None).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value

    def validate_date_of_birth(self, value):
        if value >= timezone.now().date():
            raise serializers.ValidationError("Date of birth must be in the past.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'doctor_name', 'doctor_specialization',
            'patient', 'patient_name', 'appointment_datetime',
            'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_appointment_datetime(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Appointment must be scheduled for a future date and time.")
        return value

    def validate(self, data):
        doctor = data.get('doctor')
        appointment_datetime = data.get('appointment_datetime')
        
        if doctor and appointment_datetime:
            # Check for conflicting appointments
            instance_id = self.instance.id if self.instance else None
            conflicting_appointments = Appointment.objects.filter(
                doctor=doctor,
                appointment_datetime=appointment_datetime,
                status='scheduled'
            ).exclude(pk=instance_id)
            
            if conflicting_appointments.exists():
                raise serializers.ValidationError(
                    "Doctor already has an appointment at this time."
                )
        
        return data


class AppointmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['doctor', 'patient', 'appointment_datetime', 'notes']

    def validate_appointment_datetime(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Appointment must be scheduled for a future date and time.")
        return value

    def validate(self, data):
        doctor = data.get('doctor')
        appointment_datetime = data.get('appointment_datetime')
        
        if doctor and appointment_datetime:
            conflicting_appointments = Appointment.objects.filter(
                doctor=doctor,
                appointment_datetime=appointment_datetime,
                status='scheduled'
            )
            
            if conflicting_appointments.exists():
                raise serializers.ValidationError(
                    "Doctor already has an appointment at this time."
                )
        
        return data