# ai_powered_hr_assistant/permissions.py
from rest_framework import permissions
from .models import HR, Applicants

class IsHRUserOrCandidateReadOnly(permissions.BasePermission):
    """
    Custom permission to allow:
    - HR users to perform all actions (create, update, delete, retrieve, list).
    - Candidate users to perform read-only actions (retrieve, list).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            hr = HR.objects.get(user=request.user)
            return True
        except HR.DoesNotExist:
            try:
                candidate = Applicants.objects.get(user=request.user)
                return request.method in permissions.SAFE_METHODS
            except Applicants.DoesNotExist:
                return False

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        try:
            hr = HR.objects.get(user=request.user)
            return obj.PostedByHR == hr
        except HR.DoesNotExist:
            try:
                candidate = Applicants.objects.get(user=request.user)
                return request.method in permissions.SAFE_METHODS
            except Applicants.DoesNotExist:
                return False