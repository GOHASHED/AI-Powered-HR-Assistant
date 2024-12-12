from django.contrib import admin
from django.urls import path
from .views import create_admin, get_all_applicants, recognize_employees_bulk, create_applicants

urlpatterns = [
    path('admin/', admin.site.urls),
    path('create-admin/', create_admin, name='create_admin'),
    path('create-applicants/', create_applicants, name='create_applicants'),
    path('get-applicants/', get_all_applicants, name='get_all_applicants'),
    path('recognize-employee/', recognize_employees_bulk, name='recognize_employee'),
]