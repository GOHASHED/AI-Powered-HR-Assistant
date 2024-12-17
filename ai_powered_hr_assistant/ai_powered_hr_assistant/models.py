#models.py
from django.contrib.auth.models import User
from django.db import models
from bson import ObjectId
from djongo import models  # If using Djongo

class CustomAdmin(models.Model):
    AdminID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Email = models.EmailField()
    Password = models.CharField(max_length=255)

class Organization(models.Model):
    OrganizationID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    Industry = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)

class HR(models.Model):
    HRID = models.ObjectIdField(primary_key=True, default=ObjectId)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    OrganizationName = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.user.username} - {self.OrganizationName}"

class Applicants(models.Model):
    ApplicantID = models.ObjectIdField()
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    # Email = models.EmailField()
    # Password = models.CharField(max_length=255)
    UploadedCV = models.FileField(upload_to='cvs/')

class JobAd(models.Model):
    
    class Job_Type(models.TextChoices): 
        FULL_TIME = 'FT', 'Full-Time' 
        PART_TIME = 'PT', 'Part-Time' 
        CONTRACT = 'CT', 'Contract' 
        INTERN = 'IN', 'Internship'
        
    JobAdID = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    Location = models.CharField(max_length=255)
    Pay=models.IntegerField()
    Qualification=models.TextField()
    Experience =models.TextField()
    JobType = models.CharField(
        max_length=2,
        choices=Job_Type.choices,
        default=Job_Type.FULL_TIME,
    )
    PostedByHR = models.ForeignKey(HR, on_delete=models.CASCADE)
    PostDate = models.DateTimeField(auto_now_add=True)

class CVScore(models.Model):
    ScoreID = models.AutoField(primary_key=True)
    ApplicantID = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    JobAdID = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    Score = models.FloatField()
    MatchPercentage = models.FloatField()

class Employee(models.Model):
    EmployeeID = models.ObjectIdField()
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Department = models.CharField(max_length=255)
    Position = models.CharField(max_length=255)
    OrganizationName = models.CharField(max_length=255)
    # OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)

class SentimentAnalysis(models.Model):
    AnalysisID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    SentimentScore = models.FloatField()
    FeedbackType = models.CharField(max_length=255)
    Date = models.DateTimeField()

class EmployeeRecognition(models.Model):
    RecognitionID = models.AutoField(primary_key=True)
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
    ScheduleID = models.AutoField(primary_key=True)
    ApplicantID = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    InterviewerID = models.ForeignKey(HR, on_delete=models.CASCADE)
    JobAdID = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    ScheduledTime = models.DateTimeField()

class TeamLead(models.Model):
    TeamLeadID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=255)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    CurrentProject=models.CharField(max_length=255)
    OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)
    

class Recognition(models.Model):
    RecognitionID = models.AutoField(primary_key=True)
    TeamLeadID = models.ForeignKey(TeamLead, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Remarks = models.TextField()
    Performance = models.CharField(max_length=255)
    ProjectName = models.CharField(max_length=255)
    TimeSpent = models.TimeField()
