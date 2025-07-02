# Doctor Appointment Management System

A comprehensive RESTful backend service built with Django and Django REST Framework for managing doctor appointments. This system provides API endpoints for managing doctors, patients, and appointments with MySQL database integration.

## 🚀 Features

- **Doctor Management**: Complete CRUD operations for doctor profiles
- **Patient Management**: Full patient registration and management system
- **Appointment Booking**: Seamless appointment scheduling and management
- **RESTful API**: Well-structured REST endpoints with proper HTTP methods
- **Database Integration**: MySQL database with proper relationships
- **API Documentation**: Interactive API documentation
- **Input Validation**: Comprehensive data validation and error handling
- **Admin Interface**: Django admin panel for easy management

## 🛠️ Tech Stack

- **Backend**: Django 4.x, Django REST Framework
- **Database**: MySQL 8.x
- **Language**: Python 3.8+
- **API Documentation**: Django REST Framework browsable API
- **Version Control**: Git

## 📋 Prerequisites

Before running this project, make sure you have the following installed:

- Python 3.8 or higher
- MySQL 8.x
- pip (Python package manager)
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/doctor-appointment-system.git
cd doctor-appointment-system
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

Create a MySQL database:

```sql
CREATE DATABASE doctor_db;
CREATE USER 'doctor_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON doctor_db.* TO 'doctor_user'@'localhost';
FLUSH PRIVILEGES;
```

### 5. Environment Configuration

Create a `.env` file in the root directory:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=doctor_db
DB_USER=doctor_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

### 6. Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

### 9. Run the Frontend Server

```bash
cd frontend
python -m http.server 8080
```

The API will be available at `http://localhost:8000/`
&
The Frontend will be avaiable at `http://localhost:8080/`


## 📁 Project Structure

```
doctor_appointment_system/
├── api/                          # Main API application
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── appointments/                 # Appointments app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── doctor_appointment_system/    # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── frontend/                     # Frontend Template
│   └── index.html
├── venv/                        # Virtual Environment
├── .gitignore
├── db.sqlite3
├── manage.py
├── requirements.txt
└── README.md
```

## 🔌 API Endpoints

### Doctors Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/doctors/` | Add a new doctor |
| GET | `/api/doctors/` | Get all doctors |
| GET | `/api/doctors/{id}/` | Get doctor by ID |
| PUT | `/api/doctors/{id}/` | Update doctor information |
| DELETE | `/api/doctors/{id}/` | Delete doctor |

### Patients Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/patients/` | Add a new patient |
| GET | `/api/patients/` | Get all patients |
| GET | `/api/patients/{id}/` | Get patient by ID |
| PUT | `/api/patients/{id}/` | Update patient information |
| DELETE | `/api/patients/{id}/` | Delete patient |

### Appointments Module

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/appointments/` | Book a new appointment |
| GET | `/api/appointments/` | List all appointments |
| GET | `/api/appointments/{id}/` | Get appointment details |
| DELETE | `/api/appointments/{id}/` | Cancel appointment |

## 📝 API Usage Examples

### Create a Doctor

```bash
curl -X POST http://localhost:8000/api/doctors/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. John Smith",
    "specialization": "Cardiology",
    "email": "dr.john@hospital.com",
    "phone": "+1234567890",
    "experience_years": 10
  }'
```

### Create a Patient

```bash
curl -X POST http://localhost:8000/api/patients/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@email.com",
    "phone": "+0987654321",
    "date_of_birth": "1990-05-15",
    "address": "123 Main St, City"
  }'
```

### Book an Appointment

```bash
curl -X POST http://localhost:8000/api/appointments/ \
  -H "Content-Type: application/json" \
  -d '{
    "doctor_id": 1,
    "patient_id": 1,
    "appointment_datetime": "2024-12-15T10:00:00Z",
    "reason": "Regular checkup"
  }'
```

## 🗄️ Database Schema

### Doctor Model
- `id`: Primary Key
- `name`: Doctor's full name
- `specialization`: Medical specialization
- `email`: Email address
- `phone`: Phone number
- `experience_years`: Years of experience
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Patient Model
- `id`: Primary Key
- `name`: Patient's full name
- `email`: Email address
- `phone`: Phone number
- `date_of_birth`: Date of birth
- `address`: Address
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Appointment Model
- `id`: Primary Key
- `doctor`: Foreign Key to Doctor
- `patient`: Foreign Key to Patient
- `appointment_datetime`: Appointment date and time
- `reason`: Reason for appointment
- `status`: Appointment status (scheduled, completed, cancelled)
- `created_at`: Timestamp
- `updated_at`: Timestamp

## 🧪 Testing

Run the test suite:

```bash
python manage.py test
```

Run tests for a specific app:

```bash
python manage.py test api
python manage.py test appointments
```

## 🔍 API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Django REST Framework Browsable API**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

- **Vinesh Ryapak** - *Initial work* - [Vinesh70](https://github.com/vinesh70)

## 🙏 Acknowledgments

- Django and Django REST Framework communities
- Contributors and testers
- Open source libraries used in this project

---

## System Pages

### 1. Dashboard (Homepage)
![Homepage Screenshot](S4.png)

The main dashboard provides a comprehensive overview of your medical practice with key performance indicators:

- **Total Doctors**: Displays the current number of registered doctors in the system
- **Total Patients**: Shows the complete count of registered patients
- **Scheduled Appointments**: Real-time count of upcoming appointments
- **Completed Appointments**: Track of successfully completed consultations
- **Cancelled Appointments**: Monitor of cancelled appointment statistics

This centralized view helps administrators and staff quickly assess the practice's current status and daily operations at a glance.

### 2. Doctor Management
![Doctor Screenshot](S1.png)

The doctor management module offers comprehensive functionality for managing medical professionals:

**Add New Doctors:**
- **Name**: Full name of the medical professional
- **Specialization**: Medical specialty or area of expertise
- **Phone Number**: Contact information for communication
- **Email**: Professional email address for correspondence

**Features:**
- Add new doctors to the system with complete professional details
- View all registered doctors in an organized list format
- Easy access to doctor information for appointment scheduling
- Professional profile management for each medical practitioner

### 3. Patient Management  
![Patient Screenshot](S2.png)

The patient management system provides comprehensive patient record handling:

**Patient Registration Fields:**
- **Name**: Patient's full name
- **Email**: Contact email for communication and notifications
- **Phone**: Primary contact number
- **Date of Birth**: Essential for age-related medical considerations
- **Address**: Complete residential address for records

**Capabilities:**
- Register new patients with complete demographic information
- Maintain comprehensive patient database
- View all patient details in an organized format
- Easy patient lookup for appointment scheduling
- Secure patient information management

### 4. Appointment Management
![Appointment Screenshot](S3.png)

The appointment system streamlines the scheduling and management of patient consultations:

**Booking Process:**
- **Doctor Selection**: Choose from available medical professionals
- **Patient Selection**: Select from registered patients
- **Date & Time**: Schedule appointments with preferred time slots
- **Additional Notes**: Add specific requirements or medical notes

**Appointment Actions:**
- **Complete Appointment**: Mark consultations as successfully completed
- **Cancel Appointment**: Handle appointment cancellations with proper tracking
- **View Appointments**: Monitor all scheduled, completed, and cancelled appointments

**Benefits:**
- Efficient scheduling system preventing double bookings
- Real-time appointment status tracking
- Comprehensive appointment history
- Easy rescheduling and cancellation management

## System Benefits

- **Centralized Management**: All medical practice operations in one platform
- **Real-time Updates**: Live tracking of appointments and statistics
- **User-friendly Interface**: Intuitive design for easy navigation
- **Comprehensive Records**: Complete patient and doctor information management
- **Efficient Scheduling**: Streamlined appointment booking and management
- **Status Tracking**: Monitor appointment completion and cancellation rates

## Getting Started

1. Access the dashboard to view overall system statistics
2. Add doctors and their specializations to the system
3. Register patients with complete contact information
4. Schedule appointments by selecting doctors, patients, and preferred times
5. Manage appointment status by marking them as completed or cancelled

This medical management system provides healthcare facilities with the tools needed to efficiently manage their daily operations while maintaining accurate records and improving patient care coordination.


**Happy Coding! 🚀**
