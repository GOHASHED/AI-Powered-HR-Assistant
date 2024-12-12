from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import CustomAdmin, HR, Applicants, JobAd, Recognition
import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_admin(request):
    if request.method == "POST":
        admin = CustomAdmin.objects.create(
            Name="John Doe",
            Email="admin@example.com",
            Password="hashed_password"
        )
        return JsonResponse({
            "message": "Admin created successfully",
            "admin_id": str(admin.AdminID)
        })
    else:
        return JsonResponse({
            "error": "Invalid request method. Please use POST."
        }, status=405)

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
                "applicant_id": str(applicant.ApplicantID),  # Convert ObjectId to string
                "uploaded_cv_url": applicant.UploadedCV.url
            }, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method. Please use POST."}, status=405)


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
