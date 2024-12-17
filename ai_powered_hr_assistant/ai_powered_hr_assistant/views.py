from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import CustomAdmin, HR, Applicants, JobAd, Recognition
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import UserRegistrationForm, HRProfileForm, ApplicantsProfileForm, EmployeeProfileForm

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        role = request.POST.get('role')
        print(role)
        hr_form = HRProfileForm(request.POST) if role == 'hr' else None
        applicant_form = ApplicantsProfileForm(request.POST, request.FILES) if role == 'applicant' else None
        employee_form = EmployeeProfileForm(request.POST) if role == 'employee' else None
        
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            print(user)
            
            if role == 'hr':
                print("HR Form Data: ", request.POST)
                if hr_form.is_valid():
                    hr = hr_form.save(commit=False)
                    hr.user = user
                    print("Hashir is HR+++++++++++++++++++++++", hr)
                    print(hr.user)
                    hr.save()
                else:
                    print("HR Form Errors: ", hr_form.errors)
            elif role == 'applicant':
                if applicant_form.is_valid():
                    applicant = applicant_form.save(commit=False)
                    applicant.user = user
                    applicant.save()
                else:
                    print("Applicant Form Errors: ", applicant_form.errors)
            elif role == 'employee':
                if employee_form.is_valid():
                    employee = employee_form.save(commit=False)
                    employee.user = user
                    employee.save()
                else:
                    print("Employee Form Errors: ", employee_form.errors)

            login(request, user)
            return redirect('/login')
    else:
        user_form = UserRegistrationForm()
        hr_form = HRProfileForm()
        applicant_form = ApplicantsProfileForm()
        employee_form = EmployeeProfileForm()

    return render(request, 'user_auth/register.html', {
        'user_form': user_form,
        'hr_form': hr_form,
        'applicant_form': applicant_form,
        'employee_form': employee_form,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/post-job')
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

        try:
            hr = HR.objects.get(user=request.user)
            print("Hashir is here=============================================",hr.HRID)
            hr.save()
            job_ad = JobAd(
                Title=title,
                Description=description,
                Location=location,
                Pay=pay,
                Qualification=qualification,
                Experience=experience,
                JobType=job_type,
                PostedByHR=hr
            )

            job_ad.save()  
            return redirect('/get-jobs')
        except HR.DoesNotExist:
            return JsonResponse({"error": "HR profile does not exist for this user."}, status=400)

    return render(request, 'jobs/job_ad.html')

def dashboard(request):
    return render(request, 'dashboard.html')
    
# @login_required
# def get_all_jobs(request):
#     try:
#         job_ads = JobAd.objects.all()
#         if not job_ads:
#             return JsonResponse({"message": "No job ad found"}, status=404)
#         job_ad_list = list(job_ads.values())
#         for job_ad in job_ad_list:
#             job_ad["JobAdID"] = str(job_ad["JobAdID"])
#         return JsonResponse(job_ad_list, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

@login_required
def get_all_jobs(request):
    try:
        job_ads = JobAd.objects.all()
        if not job_ads:
            return render(request, 'jobs/dashboard.html')
        return render(request, 'jobs/job_list.html', {'job_ads': job_ads})
    except Exception as e:
        return render(request, 'jobs/job_ad.html', {'error': str(e)})


# @csrf_exempt
# def create_applicants(request):
#     if request.method == "POST":
#         try:
#             name = request.POST.get("Name")
#             email = request.POST.get("Email")
#             password = request.POST.get("Password")
#             uploaded_cv = request.FILES.get("UploadedCV")
            
#             if not all([name, email, password, uploaded_cv]):
#                 return JsonResponse({"error": "All fields are required, including a CV."}, status=400)
            
#             applicant = Applicants.objects.create(
#                 Name=name,
#                 Email=email,
#                 Password=password,
#                 UploadedCV=uploaded_cv
#             )
            
#             return JsonResponse({
#                 "message": "Applicant created successfully",
#                 "applicant_id": str(applicant.ApplicantID),
#                 "uploaded_cv_url": applicant.UploadedCV.url
#             }, status=201)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

# @csrf_exempt
# def get_all_applicants(request):
#     try:
#         applicants = Applicants.objects.all()
#         if not applicants:
#             return JsonResponse({"message": "No applicants found"}, status=404)
#         applicants_list = list(applicants.values())
#         for applicant in applicants_list:
#             applicant["ApplicantID"] = str(applicant["ApplicantID"])  # Convert ApplicantID to string
#         return JsonResponse(applicants_list, safe=False)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

# @csrf_exempt
# def recognize_employees_bulk(request):
#     if request.method == "POST":
#         try:
#             data = [
#                 Recognition(
#                     TeamLeadID=1,
#                     EmployeeID=emp['EmployeeID'],
#                     Remarks=emp['Remarks'],
#                     Performance=emp['Performance'],
#                     ProjectName=emp['ProjectName'],
#                     TimeSpent=emp['TimeSpent']
#                 )
#                 for emp in request.POST.getlist('employees')
#             ]
#             Recognition.objects.bulk_create(data)
#             return JsonResponse({"message": "Bulk recognition saved successfully"})
#         except Exception as e:
#             return JsonResponse({"error": str(e)})
#     else:
#         return JsonResponse({
#             "error": "Invalid request method. Please use POST."
#         }, status=405)