# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # views.py
# from rest_framework import generics, status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User
# from .models import CustomAdmin, HR, Applicants, JobAd, Employee, JobApplication
# from .serializers import CustomAdminSerializer, HRSerializer, ApplicantsSerializer, JobAdSerializer, EmployeeSerializer
# from .forms import UserRegistrationForm, HRProfileForm, ApplicantsProfileForm, EmployeeProfileForm
# from django.core.files.storage import default_storage
# from bson.objectid import ObjectId

# @api_view(['POST'])
# def create_admin(request):
#     serializer = CustomAdminSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(Password=request.data['Password'])  # Hash password later
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def register(request):
#     user_form = UserRegistrationForm(request.data)
#     role = request.data.get('role')
#     data_ex=request.data
#     print("Data Extract===============",data_ex)
#     hr_form = HRProfileForm(request.data)
#     print("user_form", hr_form.is_valid())
#     if user_form.is_valid():
#         user = user_form.save(commit=False)
#         user.set_password(user_form.cleaned_data['password'])
#         user.save()

#         if role == 'HR':
#             hr_form = HRProfileForm(request.data)
#             if hr_form.is_valid():
#                 hr = hr_form.save(commit=False)
#                 hr.user = user
#                 hr.save()
#                 return Response({"message": "HR registered"}, status=status.HTTP_201_CREATED)
#         elif role == 'Candidate':
#             applicant_form = ApplicantsProfileForm(request.data, request.FILES)
#             if applicant_form.is_valid():
#                 applicant = applicant_form.save(commit=False)
#                 applicant.user = user
#                 applicant.save()
#                 return Response({"message": "Applicant registered"}, status=status.HTTP_201_CREATED)
#         elif role == 'Employee':
#             employee_form = EmployeeProfileForm(request.data)
#             if employee_form.is_valid():
#                 employee = employee_form.save(commit=False)
#                 employee.user = user
#                 employee.save()
#                 return Response({"message": "Employee registered"}, status=status.HTTP_201_CREATED)
#         login(request, user)
#         return Response({"message": "User registered"}, status=status.HTTP_201_CREATED)
#     return Response(user_form.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def user_login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user:
#         refresh = RefreshToken.for_user(user)
#         return Response({
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#             'role': 'HR' if HR.objects.filter(user=user).exists() else 'Employee' if Employee.objects.filter(user=user).exists() else 'Applicant'
#         }, status=status.HTTP_200_OK)
#     return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# @api_view(['POST'])
# def user_logout(request):
#     logout(request)
#     return Response({"message": "Logged out"}, status=status.HTTP_200_OK)

# @api_view(['POST'])
# def upload_cv(request):
#     try:
#         applicant = Applicants.objects.get(user=request.user)
#         if request.FILES.get('cv'):
#             if applicant.UploadedCV:
#                 default_storage.delete(applicant.UploadedCV.path)
#             applicant.UploadedCV = request.FILES['cv']
#             applicant.save()
#             return Response({"message": "CV uploaded"}, status=status.HTTP_200_OK)
#     except Applicants.DoesNotExist:
#         return Response({"error": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)
#     return Response({"error": "No CV provided"}, status=status.HTTP_400_BAD_REQUEST)

# class JobAdListCreate(generics.ListCreateAPIView):
#     queryset = JobAd.objects.all()
#     serializer_class = JobAdSerializer

#     def perform_create(self, serializer):
#         hr = HR.objects.get(user=self.request.user)
#         serializer.save(PostedByHR=hr)

# class JobAdDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = JobAd.objects.all()
#     serializer_class = JobAdSerializer

# @api_view(['POST'])
# def apply_job(request, job_id):
#     try:
#         job_id_obj = ObjectId(job_id)
#         job_ad = JobAd.objects.get(_id=job_id_obj)
#         applicant = Applicants.objects.get(user=request.user)
        
#         application = JobApplication.objects.create(
#             Applicant=applicant,
#             JobAd=job_ad,
#             Status='Pending'
#         )
#         # Add application logic if needed (e.g., save to a model)
#         return Response({"message": "Applied successfully"}, status=status.HTTP_200_OK)
#     except JobAd.DoesNotExist:
#         return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Applicants.DoesNotExist:
#         return Response({"error": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# # @csrf_exempt
# # def create_admin(request):
# #     if request.method == "POST":
# #         try:
# #             name=request.POST.get("Name")
# #             email=request.POST.get("Email")
# #             password=request.POST.get("Password")
            
# #             if not all([name, email, password]):
# #                     return JsonResponse({"error": "All fields are required."}, status=400)
            
# #             admin = CustomAdmin.objects.create(
# #                 Name=name,
# #                 Email=email,
# #                 Password=password
# #             )
            
# #             return JsonResponse({
# #                 "message": "Admin created successfully",
# #                 "admin_id": str(admin.AdminID)
# #             },status=201)
# #         except Exception as e:
# #             return JsonResponse({"error": str(e)}, status=500)
# #     return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)


# ai_powered_hr_assistant/views.py
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import CustomAdmin, HR, Applicants, JobAd, Employee, JobApplication
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
    data_ex = request.data
    print("Data Extract===============", data_ex)
    print("user_form", user_form.is_valid())
    if user_form.is_valid():
        user = user_form.save()  # This will save the user with hashed password

        if role == 'HR':
            hr_form = HRProfileForm(request.data)
            if hr_form.is_valid():
                hr = hr_form.save(commit=False)
                hr.user = user
                hr.save()
                return Response({"message": "HR registered", "hr_id": hr.id}, status=status.HTTP_201_CREATED)
        elif role == 'Candidate':
            applicant_form = ApplicantsProfileForm(request.data, request.FILES)
            if applicant_form.is_valid():
                applicant = applicant_form.save(commit=False)
                applicant.user = user
                applicant.save()
                return Response({"message": "Applicant registered", "applicant_id": applicant.id}, status=status.HTTP_201_CREATED)
        elif role == 'Employee':
            employee_form = EmployeeProfileForm(request.data)
            if employee_form.is_valid():
                employee = employee_form.save(commit=False)
                employee.user = user
                employee.save()
                return Response({"message": "Employee registered", "employee_id": employee.id}, status=status.HTTP_201_CREATED)
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
        job_ad = JobAd.objects.get(id=job_id)  # Use integer id instead of ObjectId
        applicant = Applicants.objects.get(user=request.user)
        
        application = JobApplication.objects.create(
            Applicant=applicant,
            JobAd=job_ad,
            Status='Pending'
        )
        return Response({"message": "Applied successfully", "application_id": application.id}, status=status.HTTP_200_OK)
    except JobAd.DoesNotExist:
        return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
    except Applicants.DoesNotExist:
        return Response({"error": "Applicant not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)