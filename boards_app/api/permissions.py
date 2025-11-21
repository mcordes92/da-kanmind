from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound


class IsBoardMemberOrOwner(BasePermission):
    """Permission allowing access only to board owners or members."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user in obj.members.all()

    def has_permission(self, request, view):
        # Prüfen ob das Board existiert, wenn es eine Detail-Action ist
        if view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            from boards_app.models import Boards
            pk = view.kwargs.get('pk')
            
            try:
                board = Boards.objects.get(pk=pk)
            except Boards.DoesNotExist:
                raise NotFound(detail="Board not found.")
            
            # Board existiert, aber User hat keine Berechtigung
            if board.owner != request.user and request.user not in board.members.all():
                return False
                
        return request.user and request.user.is_authenticated


class IsBoardOwner(BasePermission):
    """Permission restricting access to board owners only."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user