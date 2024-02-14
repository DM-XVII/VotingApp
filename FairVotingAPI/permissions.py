from rest_framework import permissions
class PollsPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return True
        
        return request.user and request.user.is_staff # if two conditions are true -- returns True

class DetailPollPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','PATCH']:
            return True
        
        return request.user and request.user.is_staff
    
class OnlyManagerPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff 
    
