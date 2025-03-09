# ai_powered_hr_assistant/models.py
from django.contrib.auth.models import User
from django.db import models

class CustomAdmin(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    Name = models.CharField(max_length=255)
    Email = models.EmailField(unique=True)
    Password = models.CharField(max_length=255)  # Use Django's password hashing later

    class Meta:
        db_table = 'ai_powered_hr_assistant_customadmin'

class Organization(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    Name = models.CharField(max_length=255, unique=True)
    Industry = models.CharField(max_length=255)
    Location = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_powered_hr_assistant_organization'

class HR(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    OrganizationName = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.OrganizationName}"

    class Meta:
        db_table = 'ai_powered_hr_assistant_hr'

class Applicants(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    UploadedCV = models.FileField(upload_to='cvs/', null=True, blank=True)

    class Meta:
        db_table = 'ai_powered_hr_assistant_applicants'

class JobAd(models.Model):
    class Job_Type(models.TextChoices):
        FULL_TIME = 'FT', 'Full-Time'
        PART_TIME = 'PT', 'Part-Time'
        CONTRACT = 'CT', 'Contract'
        INTERN = 'IN', 'Internship'

    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
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
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    Applicant = models.ForeignKey(Applicants, on_delete=models.CASCADE, related_name='applications')
    JobAd = models.ForeignKey(JobAd, on_delete=models.CASCADE, related_name='applications')
    ApplicationDate = models.DateTimeField(auto_now_add=True)
    Status = models.CharField(max_length=50, default='Pending')

    class Meta:
        db_table = 'ai_powered_hr_assistant_jobapplication'

class CVScore(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of ScoreID
    ApplicantID = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    JobAdID = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    Score = models.FloatField()
    MatchPercentage = models.FloatField()
    AnalysisDate = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    Notes = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'ai_powered_hr_assistant_cvscore'

class Employee(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=255)
    Department = models.CharField(max_length=255)
    Position = models.CharField(max_length=255)
    OrganizationName = models.CharField(max_length=255)

    class Meta:
        db_table = 'ai_powered_hr_assistant_employee'

class SentimentAnalysis(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    SentimentScore = models.FloatField()
    FeedbackType = models.CharField(max_length=255)
    Date = models.DateTimeField()

    class Meta:
        db_table = 'ai_powered_hr_assistant_sentimentanalysis'

class EmployeeRecognition(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    PerformanceScore = models.FloatField()
    RecognitionType = models.CharField(max_length=255)
    Date = models.DateTimeField()

    class Meta:
        db_table = 'ai_powered_hr_assistant_employeerecognition'

class Chatbot(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of ChatbotID
    Query = models.TextField()
    Response = models.TextField()
    QueryDate = models.DateTimeField()
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'ai_powered_hr_assistant_chatbot'

class InterviewSchedule(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    ApplicantID = models.ForeignKey(Applicants, on_delete=models.CASCADE)
    InterviewerID = models.ForeignKey(HR, on_delete=models.CASCADE)
    JobAdID = models.ForeignKey(JobAd, on_delete=models.CASCADE)
    ScheduledTime = models.DateTimeField()

    class Meta:
        db_table = 'ai_powered_hr_assistant_interviewschedule'

class TeamLead(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    Name = models.CharField(max_length=255)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    CurrentProject = models.CharField(max_length=255)
    OrganizationID = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class Meta:
        db_table = 'ai_powered_hr_assistant_teamlead'

class Recognition(models.Model):
    id = models.AutoField(primary_key=True)  # Use AutoField instead of _id
    TeamLeadID = models.ForeignKey(TeamLead, on_delete=models.CASCADE)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    Remarks = models.TextField()
    Performance = models.CharField(max_length=255)
    ProjectName = models.CharField(max_length=255)
    TimeSpent = models.TimeField()

    class Meta:
        db_table = 'ai_powered_hr_assistant_recognition'