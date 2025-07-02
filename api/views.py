from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from appointments.models import Doctor, Patient, Appointment
from .serializers import (
    DoctorSerializer, 
    PatientSerializer, 
    AppointmentSerializer,
    AppointmentCreateSerializer
)


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    GET: List all doctors
    POST: Create a new doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'specialization']
    ordering_fields = ['name', 'specialization', 'created_at']
    ordering = ['name']


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific doctor
    PUT: Update a specific doctor
    DELETE: Delete a specific doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def delete(self, request, *args, **kwargs):
        doctor = self.get_object()
        # Check if doctor has scheduled appointments
        if doctor.appointments.filter(status='scheduled').exists():
            return Response(
                {"error": "Cannot delete doctor with scheduled appointments"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().delete(request, *args, **kwargs)


class PatientListCreateView(generics.ListCreateAPIView):
    """
    GET: List all patients
    POST: Create a new patient
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a specific patient
    PUT: Update a specific patient
    DELETE: Delete a specific patient
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def delete(self, request, *args, **kwargs):
        patient = self.get_object()
        # Check if patient has scheduled appointments
        if patient.appointments.filter(status='scheduled').exists():
            return Response(
                {"error": "Cannot delete patient with scheduled appointments"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().delete(request, *args, **kwargs)


class AppointmentListCreateView(generics.ListCreateAPIView):
    """
    GET: List all appointments
    POST: Create a new appointment
    """
    queryset = Appointment.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['doctor', 'patient', 'status']
    search_fields = ['doctor__name', 'patient__name']
    ordering_fields = ['appointment_datetime', 'created_at']
    ordering = ['-appointment_datetime']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AppointmentCreateSerializer
        return AppointmentSerializer


class AppointmentDetailView(generics.RetrieveDestroyAPIView):
    """
    GET: Retrieve a specific appointment
    DELETE: Cancel a specific appointment
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def delete(self, request, *args, **kwargs):
        appointment = self.get_object()
        # Instead of deleting, mark as cancelled
        appointment.status = 'cancelled'
        appointment.save()
        return Response(
            {"message": "Appointment cancelled successfully"},
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def doctor_appointments(request, doctor_id):
    """
    Get all appointments for a specific doctor
    """
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return Response(
            {"error": "Doctor not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    appointments = doctor.appointments.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def patient_appointments(request, patient_id):
    """
    Get all appointments for a specific patient
    """
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return Response(
            {"error": "Patient not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    appointments = patient.appointments.all()
    serializer = AppointmentSerializer(appointments, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def complete_appointment(request, appointment_id):
    """
    Mark an appointment as completed
    """
    try:
        appointment = Appointment.objects.get(id=appointment_id)
    except Appointment.DoesNotExist:
        return Response(
            {"error": "Appointment not found"}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    if appointment.status != 'scheduled':
        return Response(
            {"error": "Only scheduled appointments can be completed"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    appointment.status = 'completed'
    appointment.save()
    
    serializer = AppointmentSerializer(appointment)
    return Response(serializer.data)


@api_view(['GET'])
def dashboard_stats(request):
    """
    Get dashboard statistics
    """
    stats = {
        'total_doctors': Doctor.objects.count(),
        'total_patients': Patient.objects.count(),
        'scheduled_appointments': Appointment.objects.filter(status='scheduled').count(),
        'completed_appointments': Appointment.objects.filter(status='completed').count(),
        'cancelled_appointments': Appointment.objects.filter(status='cancelled').count(),
    }
    return Response(stats)