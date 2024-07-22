from django import forms
from django.contrib.auth import authenticate
from .models import SpecialistClassification, CustomUser, Patientdiagnosis, Systemdiscomfort, SpecialistSpecification,Bodysystem, Systemdiscomfort,  County, SubCounty, Facility, ServiceCategory, Service, FacilityService

class SpecialistClassificationForm(forms.ModelForm):
    class Meta:
        model = SpecialistClassification
        fields = ['class_name']

class SpecialistSpecificationForm(forms.ModelForm):
    class Meta:
        model=SpecialistSpecification
        fields=['specific_name','classification']

class BodysystemForm(forms.ModelForm):
    class Meta:
        model = Bodysystem
        fields= ['system_name']

class PatientdiagnosisForm(forms.ModelForm):
    class Meta:
        model = Patientdiagnosis
        fields = ['patient' , 'system_discomfort', 'severity']
        
class PatientdiagnosisForm(forms.ModelForm):
    class Meta:
        model = Patientdiagnosis
        fields = ['patient' , 'system_discomfort', 'severity']

class PatientdiagnosisForm(forms.ModelForm):
    class Meta:
        model = Patientdiagnosis
        fields = ['patient' , 'system_discomfort', 'severity']

class SystemdiscomfortForm(forms.ModelForm):
    class Meta:
        model = Systemdiscomfort
        fields = ['discomfort_name', 'body_system']

# class SystemdiscomfortForm(forms.ModelForm):
#     cardiovascular_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Cardiovascular'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'cardiovascularSelect'}),
#         required=False
#     )
#     respiratory_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Respiratory'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'respiratorySelect'}),
#         required=False
#     )
#     gastrointestinal_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Gastrointestinal'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'gastrointestinalSelect'}),
#         required=False
#     )
#     neurological_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Neurological'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'neurologicalSelect'}),
#         required=False
#     )
#     musculoskeletal_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Musculoskeletal'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'musculoskeletalSelect'}),
#         required=False
#     )
#     dermatological_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Dermatological'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'dermatologicalSelect'}),
#         required=False
#     )
#     psychiatric_symptoms = forms.ModelMultipleChoiceField(
#         queryset=Bodysystem.objects.filter(body_system__system_name='Psychiatric'),
#         widget=forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'psychiatricSelect'}),
#         required=False
#     )

#     class Meta:
#         model = Systemdiscomfort
#         fields = ['discomfort_name', 'body_system', 'cardiovascular_symptoms', 'respiratory_symptoms',
#                   'gastrointestinal_symptoms', 'neurological_symptoms', 'musculoskeletal_symptoms', 
#                   'dermatological_symptoms', 'psychiatric_symptoms']        

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('admin', 'Admin'), ('doctor', 'Doctor'), ('nurse', 'Nurse'), ('accountant', 'Accountant')], required=False)
    specification = forms.ModelChoiceField(queryset=SpecialistSpecification.objects.all(), required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'national_identity', 'phone', 'email', 'gender', 'county', 'sub_county', 'password', 'password_confirm', 'role', 'specification']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")

        if password:
            user.set_password(password)

        if commit:
            user.save()
        return user

class CountyForm(forms.ModelForm):
    class Meta:
        model=County
        fields=['county_name']

class SubCountyForm(forms.ModelForm):
    class Meta:
        model=SubCounty
        fields=['subcountyname', 'county']

class FacilityForm(forms.ModelForm):
    class Meta:
        model=Facility
        fields=['name', 'worknumber', 'phone', 'email', 'location', 'address', 'facility_type', 'subcounty']

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model=ServiceCategory
        fields=['category_name']

class ServiceForm(forms.ModelForm):
    class Meta:
        model=Service
        fields=['name', 'category']

class FacilityServiceForm(forms.ModelForm):
    class Meta:
        model=FacilityService
        fields=['service', 'facility']

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("Invalid email or password")

        return cleaned_data