from django.shortcuts import render, redirect, get_object_or_404
from .forms import SpecialistClassificationForm, SystemdiscomfortForm, BodysystemForm, SpecialistSpecificationForm, UserForm, FacilityForm, ServiceCategoryForm,ServiceForm, CountyForm, SubCountyForm, LoginForm
from .models import SpecialistClassification,Bodysystem,Systemdiscomfort,Patientdiagnosis, Symptom, ServiceCategory, County, SubCounty, Facility,Service, CustomUser, SpecialistSpecification
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.conf import settings
from django.http import JsonResponse, HttpResponse

# Create your views here.
@login_required
def symptoms_step1(request):
    if request.method == 'POST':
        user = request.user
        selected_symptoms = {}

        for bodysystem in Bodysystem.objects.all():
            system_name_slug = bodysystem.system_name.replace(" ", "_").lower()
            symptoms = request.POST.getlist(f"{system_name_slug}_symptoms")
            selected_symptoms[system_name_slug] = symptoms

            # Store selected symptoms in session
            request.session[f"{system_name_slug}_selected_symptoms"] = symptoms

            # Save the selected symptoms with null severity
            for symptom_name in symptoms:
                try:
                    system_discomfort = Systemdiscomfort.objects.get(discomfort_name=symptom_name, body_system=bodysystem)
                    Patientdiagnosis.objects.create(
                        patient=user,
                        system_discomfort=system_discomfort,
                        severity='null'  # Default value if severity is not provided
                    )
                except Systemdiscomfort.DoesNotExist:
                    continue  # Skip if the symptom does not exist in the database

        return redirect('severity')

    bodysystems = Bodysystem.objects.all()
    return render(request, 'blog/symptoms.html', {'bodysystems': bodysystems})



@login_required
def severity(request):
    user = request.user

    if request.method == 'POST':
        # Handle form submission for severity
        diagnoses = Patientdiagnosis.objects.filter(patient=user)
        for diagnosis in diagnoses:
            severity_key = f"{slugify(diagnosis.system_discomfort.body_system.system_name)}_{slugify(diagnosis.system_discomfort.discomfort_name)}_severity"
            severity = request.POST.get(severity_key)
            if severity:
                diagnosis.severity = severity
                diagnosis.save()
        
        # Redirect to symptoms_step1
        return redirect('fetch_severity_and_facility')

    # Fetch all Patientdiagnosis records for the current user
    diagnoses = Patientdiagnosis.objects.filter(patient=user).select_related('system_discomfort__body_system')

    # Get a set of Bodysystem instances related to the diagnoses
    bodysystems = Bodysystem.objects.filter(systemdiscomfort__patientdiagnosis__in=diagnoses).distinct()

    # Group diagnoses by Bodysystem
    bodysystem_diagnoses = {}
    for diagnosis in diagnoses:
        bodysystem = diagnosis.system_discomfort.body_system
        if bodysystem not in bodysystem_diagnoses:
            bodysystem_diagnoses[bodysystem] = []
        bodysystem_diagnoses[bodysystem].append(diagnosis)

    context = {
        'bodysystem_diagnoses': bodysystem_diagnoses
    }

    return render(request, 'blog/severity_page.html', context)

@login_required
def fetch_severity_and_facility(request):
    user = request.user

    if request.method == 'POST':
        # Get the selected facility
        selected_facility_id = request.POST.get('facility')
        if selected_facility_id:
            selected_facility = Facility.objects.get(id=selected_facility_id)
            # You can save this facility selection to the user or another relevant model

        # Redirect to the desired next step
        return redirect('facility_homepage')  # Replace with the actual name of your next view

    # Fetch all Patientdiagnosis records for the current user
    diagnoses = Patientdiagnosis.objects.filter(patient=user).select_related('system_discomfort__body_system')

    # Get a set of Bodysystem instances related to the diagnoses
    bodysystems = Bodysystem.objects.filter(systemdiscomfort__patientdiagnosis__in=diagnoses).distinct()

    # Group diagnoses by Bodysystem
    bodysystem_diagnoses = {}
    for diagnosis in diagnoses:
        bodysystem = diagnosis.system_discomfort.body_system
        if bodysystem not in bodysystem_diagnoses:
            bodysystem_diagnoses[bodysystem] = []
        bodysystem_diagnoses[bodysystem].append(diagnosis)

    # Fetch all facilities
    facilities = Facility.objects.all()

    context = {
        'bodysystem_diagnoses': bodysystem_diagnoses,
        'facilities': facilities
    }

    return render(request, 'blog/fetch_severity_and_facility.html', context)


@login_required
def index(request):
    return render(request, "blog/home.html")

def facility(request):
    return render(request, "blog/facility.html")    

# @login_required
def reports(request):
    return render(request, "blog/reports.html")

def specialist(request):
    return render(request, "blog/specialist.html")

def services(request):
    return render(request, "blog/services.html")

def billing(request):
    return render(request, "blog/billing.html")

def logout(request):
    return render(request, "blog/login.html")

@login_required
def dashboard(request):
    return render(request, "blog/dashboard.html")

def enroll_facility(request):
    if request.method=="POST":
        form=FacilityForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll_facility')
    else:
        form=FacilityForm()
        subcounties=SubCounty.objects.all()
        context={
            'form':form,
            'subcounties':subcounties
        }
    return render(request, "blog/enroll_facility.html", context)

def updt(request, spec_id):
    spec = get_object_or_404(CustomUser, id=spec_id)
    
    if request.method == 'POST':
        if request.POST.get('_method') == 'PUT':
            form = UserForm(request.POST, instance=spec)
            if form.is_valid():
                form.save()
                return redirect('specialist_fetch')
        else:
            # Handle other POST request types if necessary
            pass
    else:
        form = UserForm(instance=spec)
    
    context = {
        'form': form,
        'counties': County.objects.all(),
        'sub_counties': SubCounty.objects.all(),
    }
    return render(request, 'blog/updt.html', context)

def specialist_classification(request):
    if request.method=='POST':
        form=SpecialistClassificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialist_classification')
    else:
        form=SpecialistClassificationForm()
    return render(request, "blog/specialist_classification.html", {'form':form})


def specialist_specification(request):
    if request.method=='POST':
        form=SpecialistSpecificationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('specialist_specification')
    else:
        form=SpecialistSpecificationForm()
        classifications=SpecialistClassification.objects.all()

        context={
            'form':form,
            'classifications': classifications
        }

    return render(request, "blog/specialist_specification.html", context)

def specialization_tabs(request):
    return render(request, "blog/specialization_tabs.html")

def user_table(request):
    return render(request, "blog/user_table.html")

def service_category(request):
    if request.method =='POST':
        form=ServiceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_category')
    else:
        form=ServiceCategoryForm()
    return render(request, "blog/service_category.html", {'form': form})

def service_name(request):
    if request.method=='POST':
        form=ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('service_name')
    else:
        form=ServiceForm()
        categories=ServiceCategory.objects.all()
        context={
            'form':form,
            'categories':categories
        }
    return render(request, "blog/service_name.html", context)

# @login_required
def service_fetch(request):
    services_list = Service.objects.select_related('category').all()
    paginator = Paginator(services_list, 10)  # Show 10 services per page

    page_number = request.GET.get('page')
    services = paginator.get_page(page_number)

    context = {
        'services': services
    }
    return render(request, "blog/service_fetch.html", context)

def miscellaneous(request):
    return render(request, "blog/miscellaneous.html")

def county(request):
    if request.method=='POST':
        form=CountyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('county')
    else:
        form=CountyForm()
    return render(request, "blog/county.html", {'form':form})

def sub_county(request):
    if request.method=='POST':
        form=SubCountyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sub_county')
    else:
        form=SubCountyForm()
        counties=County.objects.all()
        context={
            'form':form,
            'counties':counties
        }
    return render(request, "blog/sub_county.html", context)

def county_fetch(request):
    subcounties_list = SubCounty.objects.select_related('county').all()
    paginator = Paginator(subcounties_list, 10)  # Show 10 subcounties per page

    page_number = request.GET.get('page')
    subcounties = paginator.get_page(page_number)

    context = {
        'subcounties': subcounties
    }
    return render(request, "blog/county_fetch.html", context)

# @login_required
def facility_fetch(request):
    facilities=Facility.objects.all()
    context={
        'facilities':facilities
    }
    return render(request, "blog/facility_fetch.html", context)

def specialist_fetch(request):
    specs=CustomUser.objects.select_related('county', 'sub_county').all()
    context={
        'specs':specs
    }
    return render(request, "blog/specialist_fetch.html", context)

def delete(request, user_id):
    user=get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('specialist_fetch')

def delt(request, fac_id):
    user=get_object_or_404(Facility, id=fac_id)
    user.delete()
    return redirect('facility_fetch')



def update(request, facility_id):
    facility=get_object_or_404(Facility, id=facility_id)
    if request.method=="POST":
        if request.POST.get('_method')=='PUT':
            form=FacilityForm(request.POST, instance=facility)
            if form.is_valid():
                form.save()
                return redirect('facility_table_div')
    else:
        form=FacilityForm(instance=facility)
    context={
        'form':form,
        'subcounties':SubCounty.objects.all()
    }

    return render(request, "blog/update.html", context)

def facility_table_div(request):
    facility=get_object_or_404(Facility, id=1)
    context={
        'facility':facility
    }
    return render(request, "blog/facility_table_div.html", context)

# @login_required
def render_specialist_details(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('render_specialist_details')
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, "blog/render_specialist_details.html", {'form':form})

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if user.role is None:
                user.role = 'patient'  # Default to patient if role is not specified
            user.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'blog/register.html', {'form': form})

def session_start(request, user):
    request.session['user_id'] = user.id
    request.session['role'] = user.role

def session_destroy(request):
    request.session.flush()

def session_end(request):
    request.session.clear_expired()

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                auth_login(request, user)
                session_start(request, user)
                if user.role == 'patient':
                    print("Redirecting to home")
                    return redirect('home')
                else:
                    print("Redirecting to dashboard")
                    return redirect('dashboard')
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('login')

def facility_homepage(request):
    facilities=Facility.objects.all()
    context={
        'facilities': facilities
    }
    return render(request, "blog/facility_homepage.html", context)

def profile_homepage(request):
    user=get_object_or_404(CustomUser, id=24)
    context={
        'user':user
    }
    return render(request, "blog/profile_homepage.html", context)

def medical_ailment(request):
    return render(request, "blog/medical_ailment.html")

def ailment_body_system(request):
    if request.method=='POST':
        form=BodysystemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ailment_body_system')
    else:
        form=BodysystemForm()
    return render(request, "blog/ailment_body_system.html", {'form':form})

def ailment_system_discomfort(request):
    if request.method=='POST':
        form=SystemdiscomfortForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ailment_system_discomfort')
    else:
        form=SystemdiscomfortForm()
        systems=Bodysystem.objects.all()
        context={
            'form':form,
            'systems':systems
        }
    return render(request, "blog/ailment_system_discomfort.html", context)


def fetch_symptoms(request):
    body_system_id = request.GET.get('body_system_id')
    if body_system_id:
        symptoms = Systemdiscomfort.objects.filter(body_system_id=body_system_id).values('id', 'discomfort_name')
        return JsonResponse(list(symptoms), safe=False)
    return JsonResponse([], safe=False)