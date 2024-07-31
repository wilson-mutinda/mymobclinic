from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password



class SpecialistClassification(models.Model):
    class_name = models.CharField(max_length=50)

    def __str__(self):
        return self.class_name

class SpecialistSpecification(models.Model):
    specific_name = models.CharField(max_length=50)
    classification = models.ForeignKey(SpecialistClassification, on_delete=models.CASCADE)

    def __str__(self):
        return self.specific_name
    

class County(models.Model):
    county_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.county_name

class SubCounty(models.Model):
    subcountyname = models.CharField(max_length=50)
    county = models.ForeignKey(County, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcountyname

class Facility(models.Model):
    name = models.CharField(max_length=50)
    worknumber = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    location = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    facility_type = models.CharField(max_length=255)
    subcounty = models.ForeignKey(SubCounty, on_delete=models.CASCADE)



class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
        ('nurse', 'Nurse'),
        ('accountant', 'Accountant'), 
     # if you have admin role
    ]
    role = models.CharField(max_length=40, choices=ROLE_CHOICES, default='patient')
    national_identity = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=15)
    county = models.ForeignKey(County, on_delete=models.SET_NULL, null=True, blank=True)
    sub_county = models.ForeignKey(SubCounty, on_delete=models.SET_NULL, null=True, blank=True)
    facility = models.ForeignKey(Facility, on_delete=models.SET_NULL, null=True, blank=True)
    specification = models.ForeignKey(SpecialistSpecification, on_delete=models.SET_NULL, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    def __str__(self):
        return self.username

class Bodysystem(models.Model):
  system_name=models.CharField(max_length=254)

  def __str__(self):
    return self.system_name
    
class Systemdiscomfort(models.Model):
    discomfort_name=models.CharField(max_length=254)
    body_system=models.ForeignKey(Bodysystem, on_delete=models.CASCADE)

    def __str__(self):
        return self.discomfort_name

class Symptom(models.Model):
    body_system = models.ForeignKey(Bodysystem, on_delete=models.CASCADE)
    symptom_name = models.CharField(max_length=254)

    def __str__(self):
        return self.symptom_name

class Patientdiagnosis(models.Model):
    patient=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    system_discomfort=models.ForeignKey(Systemdiscomfort, on_delete=models.CASCADE)
    severity=models.CharField(max_length=254, default='null')


class ServiceCategory(models.Model):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name

class Service(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE)

class FacilityService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

class Appeal(models.Model):
    patient_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE)
    appeal_date = models.DateTimeField()
    appeal_status = models.CharField(max_length=254, default='pending')
    payment_status = models.CharField(max_length=254, default='null')

    def __str__(self):
        return f'Appeal for {self.facility_id.name} by {self.patient_id.username}'
    
class Appeal_Assignment(models.Model):
    patient=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_patient')
    appeal=models.ForeignKey(Appeal, on_delete=models.CASCADE)
    specialist=models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_specialist')



    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        verbose_name='groups',
        blank=True,
        help_text='user groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        verbose_name='permissions',
        blank=True,
        help_text='user permissions',
        related_query_name='user permissions',
    )


