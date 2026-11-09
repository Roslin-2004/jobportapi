from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    message="only owner can update and delete records"
    def has_permission(self,request,view):
        if(request.method=="GET"):
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if(request.method=="GET"):
            return True
        return obj.postedby == request.user