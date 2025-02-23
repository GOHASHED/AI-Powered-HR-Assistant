from rest_framework import serializers
from .models import CustomAdmin, HR, Applicants, JobAd, Employee

class CustomAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomAdmin
        fields = ['AdminID', 'Name', 'Email']

class HRSerializer(serializers.ModelSerializer):
    class Meta:
        model = HR
        fields = ['HRID', 'Name', 'OrganizationName', 'user']

class ApplicantsSerializer(serializers.ModelSerializer):
    UploadedCV = serializers.FileField(required=False)
    class Meta:
        model = Applicants
        fields = ['ApplicantID', 'Name', 'UploadedCV', 'user']

class JobAdSerializer(serializers.ModelSerializer):
    PostedByHR = HRSerializer(read_only=True)
    class Meta:
        model = JobAd
        fields = ['_id', 'Title', 'Description', 'Location', 'Pay', 'Qualification', 'Experience', 'JobType', 'PostedByHR', 'PostDate']

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['EmployeeID', 'Name', 'Department', 'Position', 'OrganizationName', 'user']