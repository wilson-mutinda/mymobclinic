from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns=[
    path('render_specialist_details', views.render_specialist_details, name='render_specialist_details'),
    path('', views.index, name='home'),
    path('symptoms', views.symptoms, name='symptoms'),
    path('facility', views.facility, name='facility'),
    path('reports', views.reports, name='reports'),
    path('specialist', views.specialist, name='specialist'),
    path('services', views.services, name='services'),
    path('billing', views.billing, name='billing'),
    path('logout', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('enroll_facility', views.enroll_facility, name='enroll_facility'),
    path('specialist_classification', views.specialist_classification, name='specialist_classification'),
    path('specialist_specification', views.specialist_specification, name='specialist_specification'),
    path('specialization_tabs', views.specialization_tabs, name='specialization_tabs'),
    path('user_table', views.user_table, name='user_table'),
    path('service_category', views.service_category, name='service_category'),
    path('service_name', views.service_name, name='service_name'),
    path('miscellaneous', views.miscellaneous, name='miscellaneous'),
    path('county', views.county, name='county'),
    path('sub_county', views.sub_county, name='sub_county'),
    path('facility_fetch', views.facility_fetch, name='facility_fetch'),
    path('specialist_fetch', views.specialist_fetch, name='specialist_fetch'),
    path('delete/<int:user_id>', views.delete, name='delete'),
    path('delt/<int:fac_id>', views.delt, name='delt'),
    path('update/<int:facility_id>', views.update, name='update'),
    path('updt/<int:spec_id>', views.updt, name='updt'),
    path('service_fetch', views.service_fetch, name='service_fetch'),
    path('county_fetch', views.county_fetch, name='county_fetch'),
    path('facility_table_div', views.facility_table_div, name='facility_table_div'),
    path('register', views.register, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout', views.logout, name='logout'),
    path('facility_homepage', views.facility_homepage, name='facility_homepage'),
    path('profile_homepage', views.profile_homepage, name='profile_homepage'),
    path('medical_ailment', views.medical_ailment, name='medical_ailment'),
    path('ailment_body_system', views.ailment_body_system, name='ailment_body_system'),
    path('ailment_system_discomfort', views.ailment_system_discomfort, name='ailment_system_discomfort'),
    path('fetch_symptoms', views.fetch_symptoms, name='fetch_symptoms'),
    # path('symptoms_step1/', views.symptoms_step1, name='symptoms_step1'),
    # path('symptoms_step2/', views.symptoms_step2, name='symptoms_step2'),
]