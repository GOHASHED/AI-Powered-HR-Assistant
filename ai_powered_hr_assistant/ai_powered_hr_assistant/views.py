# from django.shortcuts import render,redirect
# from django.http import JsonResponse
# from .models import CustomAdmin, HR, Applicants, JobAd, Recognition, Employee
# from django.contrib.auth import login
# from django.contrib.auth.models import User
# import json
# from bson import ObjectId
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth import login, authenticate, logout
# from .forms import UserRegistrationForm, HRProfileForm, ApplicantsProfileForm, EmployeeProfileForm
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile


from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CustomAdmin, HR, Applicants, JobAd, Employee
from .serializers import CustomAdminSerializer, HRSerializer, ApplicantsSerializer, JobAdSerializer, EmployeeSerializer
from .forms import UserRegistrationForm, HRProfileForm, ApplicantsProfileForm, EmployeeProfileForm
from django.core.files.storage import default_storage

@api_view(['POST'])
def create_admin(request):
    serializer = CustomAdminSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(Password=request.data['Password'])  # Hash password later
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register(request):
    user_form = UserRegistrationForm(request.data)
    role = request.data.get('role')

    if user_form.is_valid():
        user = user_form.save(commit=False)
        user.set_password(user_form.cleaned_data['password'])
        user.save()

        if role == 'HR':
            hr_form = HRProfileForm(request.data)
            if hr_form.is_valid():
                hr = hr_form.save(commit=False)
                hr.user = user
                hr.save()
                return Response({"message": "HR registered"}, status=status.HTTP_201_CREATED)
        elif role == 'Candidate':
            applicant_form = ApplicantsProfileForm(request.data, request.FILES)
            if applicant_form.is_valid():
                applicant = applicant_form.save(commit=False)
                applicant.user = user
                applicant.save()
                return Response({"message": "Applicant registered"}, status=status.HTTP_201_CREATED)
        elif role == 'Employee':
            employee_form = EmployeeProfileForm(request.data)
            if employee_form.is_valid():
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
                return Response({"message": "Employee registered"}, status=status.HTTP_201_CREATED)
        login(request, user)
        return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
    return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': 'HR' if HR.objects.filter(user=user).exists() else 'Employee' if Employee.objects.filter(user=user).exists() else 'Applicant'
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({"message": "Logged out"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_cv(request):
    try:
        applicant = Applicants.objects.get(user=request.user)
        if request.FILES.get('cv'):
            if applicant.UploadedCV:
                default_storage.delete(applicant.UploadedCV.path)
            applicant.UploadedCV = request.FILES['cv']
            applicant.save()
            return Response({"message": "CV uploaded"}, status=status.HTTP_200_OK)
    except Applicants.DoesNotExist:
        return Response({"error": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)
    return Response({"error": "No CV provided"}, status=status.HTTP_400_BAD_REQUEST)

class JobAdListCreate(generics.ListCreateAPIView):
    queryset = JobAd.objects.all()
    serializer_class = JobAdSerializer

    def perform_create(self, serializer):
        hr = HR.objects.get(user=self.request.user)
        serializer.save(PostedByHR=hr)

class JobAdDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobAd.objects.all()
    serializer_class = JobAdSerializer

@api_view(['POST'])
def apply_job(request, job_id):
    try:
        job_ad = JobAd.objects.get(_id=job_id)
        applicant = Applicants.objects.get(user=request.user)
        # Add application logic if needed (e.g., save to a model)
        return Response({"message": "Applied successfully"}, status=status.HTTP_200_OK)
    except JobAd.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Applicants.DoesNotExist:
        return Response({"error": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)





# def upload_cv(request):
#     if request.method == 'POST' and request.FILES.get('cv'):
#         applicant = Applicants.objects.get(user=request.user)
        
#         # Delete the old CV if exists
#         if applicant.UploadedCV:
#             old_path = applicant.UploadedCV.path
#             if default_storage.exists(old_path):
#                 default_storage.delete(old_path)

#         # Save the new CV
#         applicant.UploadedCV = request.FILES['cv']
#         applicant.save()

#         return redirect('/jobs')  # Redirect back to jobs page

#     return render(request, 'jobs/upload_cv.html')

# def register(request):
#     data = request.data
#     user_form = UserRegistrationForm(data)
#     role = data.get('role')

#     hr_form = HRProfileForm(data) if role == 'HR' else None
#     applicant_form = ApplicantsProfileForm(data, request.FILES) if role == 'Candidate' else None
#     employee_form = EmployeeProfileForm(data) if role == 'Employee' else None

#     if user_form.is_valid():
#         user = user_form.save(commit=False)
#         user.set_password(user_form.cleaned_data['password'])
#         user.save()

#         if role == 'HR' and hr_form and hr_form.is_valid():
#             hr = hr_form.save(commit=False)
#             hr.user = user
#             hr.save()
#         elif role == 'Candidate' and applicant_form and applicant_form.is_valid():
#             applicant = applicant_form.save(commit=False)
#             applicant.user = user
#             applicant.save()
#         elif role == 'Employee' and employee_form and employee_form.is_valid():
#             employee = employee_form.save(commit=False)
#             employee.user = user
#             employee.save()

#         login(request, user)
#         return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
#     return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
            
#             # Check if the user is an HR
#             if HR.objects.filter(user=user).exists():
#                 return redirect('/post-job')
            
#             # Check if the user is an Employee
#             elif Employee.objects.filter(user=user).exists():
#                 return redirect('/dashboard')

#             # Check if the user is an Applicant
#             elif Applicants.objects.filter(user=user).exists():
#                 return redirect('/get-jobs')

#         else:
#             return render(request, 'user_auth/login.html', {'error': 'Invalid credentials'})
#     return render(request, 'user_auth/login.html')

# def user_logout(request):
#     logout(request)
#     return redirect('/login')

# @csrf_exempt
# def create_admin(request):
#     if request.method == "POST":
#         try:
#             name=request.POST.get("Name")
#             email=request.POST.get("Email")
#             password=request.POST.get("Password")
            
#             if not all([name, email, password]):
#                     return JsonResponse({"error": "All fields are required."}, status=400)
            
#             admin = CustomAdmin.objects.create(
#                 Name=name,
#                 Email=email,
#                 Password=password
#             )
            
#             return JsonResponse({
#                 "message": "Admin created successfully",
#                 "admin_id": str(admin.AdminID)
#             },status=201)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=500)
#     return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)

# @login_required
# def post_job_ad(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
#         location = request.POST['location']
#         pay = request.POST['pay']
#         qualification = request.POST['qualification']
#         experience = request.POST['experience']
#         job_type = request.POST['job_type']

#         try:
#             hr = HR.objects.get(user=request.user)
#             print("Hashir is here=============================================",hr.HRID)
#             hr.save()
#             job_ad = JobAd(
#                 Title=title,
#                 Description=description,
#                 Location=location,
#                 Pay=pay,
#                 Qualification=qualification,
#                 Experience=experience,
#                 JobType=job_type,
#                 PostedByHR=hr
#             )

#             job_ad.save()  
#             return redirect('/get-jobs')
#         except HR.DoesNotExist:
#             return JsonResponse({"error": "HR profile does not exist for this user."}, status=400)

#     return render(request, 'jobs/job_ad.html')

# def dashboard(request):
#     return render(request, 'dashboard.html')

# @login_required
# def get_all_jobs(request):
#     try:
#         job_ads = JobAd.objects.all()
#         if not job_ads:
#             return render(request, 'jobs/dashboard.html')
#         return render(request, 'jobs/job_list.html', {'job_ads': job_ads})
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=500)

# @login_required 
# @csrf_exempt 
# def apply_job(request, job_id): 
#     try:
#         job_ad = JobAd.objects.get(pk=ObjectId(job_id)) 
#         print("Job AD ID: ",job_ad)
#         applicant = Applicants.objects.get(user=request.user) 
#         applicant.save() # Logic to handle the job application can be added here 
#         return redirect('/jobs') 
#     except JobAd.DoesNotExist: 
#         return JsonResponse({"error": "Job ad not found"}, status=404) 
#     except Applicants.DoesNotExist: 
#         return JsonResponse({"error": "Applicant profile does not exist"}, status=400) 
#     except Exception as e: 
#         return JsonResponse({"error": str(e)}, status=500)
    