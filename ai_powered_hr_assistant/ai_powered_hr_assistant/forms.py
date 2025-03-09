# ai_powered_hr_assistant/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import HR, Applicants, Employee

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class HRProfileForm(forms.ModelForm):
    class Meta:
        model = HR
        fields = ['Name', 'OrganizationName']
        widgets = {
            'Name': forms.TextInput(attrs={'id': 'hr_name'}),
            'OrganizationName': forms.TextInput(attrs={'id': 'hr_organization'}),
        }

class ApplicantsProfileForm(forms.ModelForm):
    class Meta:
        model = Applicants
        fields = ['Name', 'UploadedCV']
        widgets = {
            'Name': forms.TextInput(attrs={'id': 'applicant_name'}),
        }

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['Name', 'Department', 'Position', 'OrganizationName']
        widgets = {
            'Name': forms.TextInput(attrs={'id': 'employee_name'}),
            'OrganizationName': forms.TextInput(attrs={'id': 'employee_organization'}),
        }