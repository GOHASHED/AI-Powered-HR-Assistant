from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import CustomAdmin, HR, Applicants, JobAd, Recognition
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, HRProfileForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        hr_form = HRProfileForm(request.POST)
        if user_form.is_valid() and hr_form.is_valid():
            # Save the User instance
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Create HR profile
            hr = hr_form.save(commit=False)
            hr.user = user
            hr.save()

            # Log in the user and redirect
            login(request, user)
            return redirect('/login')  # Replace with your desired redirect URL
    else:
        user_form = UserRegistrationForm()
        hr_form = HRProfileForm()

    return render(request, 'user_auth/register.html', {
        'user_form': user_form,
        'hr_form': hr_form,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/post-job')  # Replace with your desired redirect URL
        else:
            return render(request, 'user_auth/login.html', {'error': 'Invalid credentials'})
    return render(request, 'user_auth/login.html')

def user_logout(request):
    logout(request)
    return redirect('/login')

@csrf_exempt
def create_admin(request):
    if request.method == "POST":
        try:
            name=request.POST.get("Name")
            email=request.POST.get("Email")
            password=request.POST.get("Password")
            
            if not all([name, email, password]):
                    return JsonResponse({"error": "All fields are required."}, status=400)
            
            admin = CustomAdmin.objects.create(
                Name=name,
                Email=email,
                Password=password
            )
            
            return JsonResponse({
                "message": "Admin created successfully",
                "admin_id": str(admin.AdminID)
            },status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

@csrf_exempt
def create_applicants(request):
    if request.method == "POST":
        try:
            name = request.POST.get("Name")
            email = request.POST.get("Email")
            password = request.POST.get("Password")
            uploaded_cv = request.FILES.get("UploadedCV")
            
            if not all([name, email, password, uploaded_cv]):
                return JsonResponse({"error": "All fields are required, including a CV."}, status=400)
            
            applicant = Applicants.objects.create(
                Name=name,
                Email=email,
                Password=password,
                UploadedCV=uploaded_cv
            )
            
            return JsonResponse({
                "message": "Applicant created successfully",
                "applicant_id": str(applicant.ApplicantID),
                "uploaded_cv_url": applicant.UploadedCV.url
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

import logging

logger = logging.getLogger(__name__)
@login_required
def post_job_ad(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        location = request.POST['location']
        pay = request.POST['pay']
        qualification = request.POST['qualification']
        experience = request.POST['experience']
        job_type = request.POST['job_type']

        # Fetch the HR profile of the logged-in user
        try:
            hr = HR.objects.get(user=request.user)
            logger.debug(f"HR Profile: {hr}")

            # Explicitly save the HR object (just in case)
            hr.save()

            # Create the job ad
            job_ad = JobAd(
                Title=title,
                Description=description,
                Location=location,
                Pay=pay,
                Qualification=qualification,
                Experience=experience,
                JobType=job_type,
                PostedByHR=hr  # Link to the HR instance
            )

            # Explicitly save the job ad object
            job_ad.save()  # Ensure HR is properly linked before saving
            # Redirect to the job listing page or success page
            return redirect('/get-jobs')  # Or replace with 'success_page'
        except HR.DoesNotExist:
            return JsonResponse({"error": "HR profile does not exist for this user."}, status=400)

    return render(request, 'jobs/job_ad.html')

def dashboard(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def get_all_applicants(request):
    try:
        applicants = Applicants.objects.all()
        if not applicants:
            return JsonResponse({"message": "No applicants found"}, status=404)
        applicants_list = list(applicants.values())
        for applicant in applicants_list:
            applicant["ApplicantID"] = str(applicant["ApplicantID"])  # Convert ApplicantID to string
        return JsonResponse(applicants_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@login_required
def get_all_jobs(request):
    try:
        job_ads = JobAd.objects.all()
        if not job_ads:
            return JsonResponse({"message": "No job ad found"}, status=404)
        job_ad_list = list(job_ads.values())
        for job_ad in job_ad_list:
            job_ad["JobAdID"] = str(job_ad["JobAdID"])  # Convert ApplicantID to string
        return JsonResponse(job_ad_list, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def recognize_employees_bulk(request):
    if request.method == "POST":
        try:
            data = [
                Recognition(
                    TeamLeadID=1,
                    EmployeeID=emp['EmployeeID'],
                    Remarks=emp['Remarks'],
                    Performance=emp['Performance'],
                    ProjectName=emp['ProjectName'],
                    TimeSpent=emp['TimeSpent']
                )
                for emp in request.POST.getlist('employees')
            ]
            Recognition.objects.bulk_create(data)
            return JsonResponse({"message": "Bulk recognition saved successfully"})
        except Exception as e:
            return JsonResponse({"error": str(e)})
    else:
        return JsonResponse({
            "error": "Invalid request method. Please use POST."
        }, status=405)