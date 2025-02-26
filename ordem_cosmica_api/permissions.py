from rest_framework import permissions
from . import models
class IsOwner(permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.user and request.user.is_authenticated:
            try:
                if obj.author:  
                    return obj.author == models.Profile.objects.filter(user=request.user).first()
            except AttributeError:
                pass 

            try:
                if obj.user:  
                    return obj.user == request.user
            except AttributeError:
                pass 
        else:
            return False