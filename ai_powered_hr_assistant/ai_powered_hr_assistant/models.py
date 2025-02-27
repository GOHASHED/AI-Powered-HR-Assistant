#models.py
from django.contrib.auth.models import User
from django.db import models
from bson import ObjectId
from djongo import models

class CustomAdmin(models.Model):
    _id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=255)  # Use Django's password hashing later

class Organization(models.Model):
    _id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255, unique=True)
    Industry = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)

class HR(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    OrganizationName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.OrganizationName}"

class Applicants(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    UploadedCV = models.FileField(upload_to='cvs/', null=True, blank=True)

class JobAd(models.Model):
    class Job_Type(models.TextChoices):
        FULL_TIME = 'FT', 'Full-Time'
        PART_TIME = 'PT', 'Part-Time'
        CONTRACT = 'CT', 'Contract'
        INTERN = 'IN', 'Internship'

    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    Location = models.CharField(max_length=255)
    Pay = models.IntegerField()
    Qualification = models.TextField()
    Experience = models.TextField()
    JobType = models.CharField(max_length=2, choices=Job_Type.choices, default=Job_Type.FULL_TIME)
    PostedByHR = models.ForeignKey(HR, on_delete=models.CASCADE)
    PostDate = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_powered_hr_assistant_jobad'

class JobApplication(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    Applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applications')
    JobAd = models.ForeignKey(JobAd, on_delete=models.CASCADE, related_name='applications')
    ApplicationDate = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50, default='Pending')  # e.g., 'Pending', 'Reviewed', 'Accepted', 'Rejected'

# class Applicants(models.Model):
#     ApplicantID = models.ObjectIdField(primary_key=True, default=ObjectId)
#     user= models.OneToOneField(User,on_delete=models.CASCADE)
#     Name = models.CharField(max_length=255)
#     UploadedCV = models.FileField(upload_to='cvs/',null=True, blank=True)
#     def save(self, *args, **kwargs):
#         # if not self.ApplicantID:
#         #     self.ApplicantID = ObjectId()  # Generate an ObjectId if it doesn't exist
#         super().save(*args, **kwargs)

class CVScore(models.Model):
    ScoreID = models.AutoField(primary_key=True)
    ApplicantID = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    JobAdID = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    Score = models.FloatField()
    MatchPercentage = models.FloatField()
    AnalysisDate = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    Notes = models.TextField(null=True, blank=True)

class Employee(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Department = models.CharField(max_length=255)
    Position = models.CharField(max_length=255)
    OrganizationName = models.CharField(max_length=255)
    # OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)

class SentimentAnalysis(models.Model):
    _id = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    SentimentScore = models.FloatField()
    FeedbackType = models.CharField(max_length=255)
    Date = models.DateTimeField()

class EmployeeRecognition(models.Model):
    _id = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    PerformanceScore = models.FloatField()
    RecognitionType = models.CharField(max_length=255)
    Date = models.DateTimeField()

class Chatbot(models.Model):
    ChatbotID = models.AutoField(primary_key=True)
    Query = models.TextField()
    Response = models.TextField()
    QueryDate = models.DateTimeField()
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)

class InterviewSchedule(models.Model):
    _id = models.AutoField(primary_key=True)
    ApplicantID = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    InterviewerID = models.ForeignKey(HR, on_delete=models.CASCADE)
    JobAdID = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    ScheduledTime = models.DateTimeField()

class TeamLead(models.Model):
    _id = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    CurrentProject=models.CharField(max_length=255)
    OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    

class Recognition(models.Model):
    _id = models.AutoField(primary_key=True)
    TeamLeadID = models.ForeignKey(TeamLead, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Remarks = models.TextField()
    Performance = models.CharField(max_length=255)
    ProjectName = models.CharField(max_length=255)
    TimeSpent = models.TimeField()
