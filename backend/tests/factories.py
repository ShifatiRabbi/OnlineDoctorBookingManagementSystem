import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from branches.models import Branch
from doctors.models import Doctor, Specialty
from patients.models import Patient
from appointments.models import Appointment

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.Sequence(lambda n: f'user{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')
    role = 'EMPLOYEE'
    is_active = True

class AdminUserFactory(UserFactory):
    role = 'ADMIN'
    is_staff = True
    is_superuser = True

class DoctorUserFactory(UserFactory):
    role = 'DOCTOR'

class BranchFactory(DjangoModelFactory):
    class Meta:
        model = Branch
    
    name = factory.Sequence(lambda n: f'Branch {n}')
    slug = factory.Sequence(lambda n: f'branch-{n}')
    address = factory.Faker('address')
    phones = '+8801712345678'

class SpecialtyFactory(DjangoModelFactory):
    class Meta:
        model = Specialty
    
    name = factory.Sequence(lambda n: f'Specialty {n}')

class DoctorFactory(DjangoModelFactory):
    class Meta:
        model = Doctor
    
    user = factory.SubFactory(DoctorUserFactory)
    degrees = 'MBBS, MD'
    fee = 500.00
    active = True
    default_branch = factory.SubFactory(BranchFactory)
    
    @factory.post_generation
    def specialties(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for specialty in extracted:
                self.specialties.add(specialty)

class PatientFactory(DjangoModelFactory):
    class Meta:
        model = Patient
    
    name = factory.Faker('name')
    phone = factory.Sequence(lambda n: f'+880171234{n:04d}')
    address = factory.Faker('address')
    gender = 'M'

class AppointmentFactory(DjangoModelFactory):
    class Meta:
        model = Appointment
    
    patient = factory.SubFactory(PatientFactory)
    doctor = factory.SubFactory(DoctorFactory)
    branch = factory.SubFactory(BranchFactory)
    date = factory.Faker('date_this_year')
    time = factory.Faker('time')
    status = 'PENDING'
    created_by = factory.SubFactory(UserFactory)