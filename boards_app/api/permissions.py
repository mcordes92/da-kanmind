from rest_framework.permissions import BasePermission

# Permission allowing access only to board owners or members
class IsBoardMemberOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.members.all()

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

# Permission restricting access to board owners only
class IsBoardOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user