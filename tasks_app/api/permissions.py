from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotFound

from boards_app.models import Boards
from tasks_app.models import Tasks

# Permission allowing only the board owner to perform actions
class IsBoardOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user

class IsTaskBoardMember(BasePermission):
    """
    Permission that checks if user is member or owner of the board that the task belongs to
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Bei POST: board_id aus request.data prüfen
        if view.action == 'create':
            board_id = request.data.get('board')
            
            if not board_id:
                return True  # Wird später vom Serializer validiert
            
            try:
                board = Boards.objects.get(pk=board_id)
            except Boards.DoesNotExist:
                raise NotFound(detail="Board not found.")
            
            # Board existiert, aber User hat keine Berechtigung
            if board.owner != request.user and request.user not in board.members.all():
                return False
        
        return True
    
    def has_object_permission(self, request, view, obj):        
        try:
            board = Boards.objects.get(pk=obj.board.id)
        except Boards.DoesNotExist:
            raise NotFound(detail="Board not found.")
        
        return board.owner == request.user or request.user in board.members.all()
    
# Permission allowing only the task assignee to perform actions
class IsTaskOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.assignee_id == request.user
    
# Permission restricting access to comment authors only
class IsTaskCommentAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user