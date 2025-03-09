# ai_powered_hr_assistant/serializers.py
from rest_framework import serializers
from .models import CustomAdmin, HR, Applicants, JobAd, Employee

class CustomAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAdmin
        fields = ['id', 'Name', 'Email']  # Use 'id' instead of '_id'

class HRSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = ['id', 'Name', 'OrganizationName', 'user']

class ApplicantsSerializer(serializers.ModelSerializer):
    UploadedCV = serializers.FileField(required=False)
    class Meta:
        model = Applicants
        fields = ['id', 'Name', 'UploadedCV', 'user']

class JobAdSerializer(serializers.ModelSerializer):
    PostedByHR = HRSerializer(read_only=True)
    class Meta:
        model = JobAd
        fields = ['id', 'Title', 'Description', 'Location', 'Pay', 'Qualification', 'Experience', 'JobType', 'PostedByHR', 'PostDate']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'Name', 'Department', 'Position', 'OrganizationName', 'user']