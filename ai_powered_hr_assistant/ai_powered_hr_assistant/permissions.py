# ai_powered_hr_assistant/permissions.py
from rest_framework.permissions import BasePermission
from .models import HR, JobAd

class IsHRUser(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return HR.objects.filter(user=request.user).exists()
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if isinstance(obj, JobAd):
            hr = HR.objects.filter(user=request.user).first()
            return hr and obj.PostedByHR == hr
        return False