from rest_framework.permissions import BasePermission

from boards_app.models import Boards
from tasks_app.models import Tasks

# Permission allowing only the board owner to perform actions
class IsBoardOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user

# Permission verifying user is a board member or owner
class IsBoardMember(BasePermission):

    def has_permission(self, request, view):
        board = None

        data = getattr(request, "data", {}) or {}

        board_id = data.get("board")

        if board_id:
            try:
                board = Boards.objects.get(id=board_id)
            except Boards.DoesNotExist:
                return False
            
        # Fall back to determining board from task if board_id not in request
        if not board:
            task_id = view.kwargs.get("pk") or view.kwargs.get("task_pk")
            if task_id:
                try:
                    board = Tasks.objects.get(pk=task_id).board
                except Tasks.DoesNotExist:
                    return False
                
        if not board:
            return False
        
        return board.members.filter(id=request.user.id).exists() or board.owner == request.user
    
# Permission allowing only the task assignee to perform actions
class IsTaskOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.assignee_id == request.user
    
# Permission restricting access to comment authors only
class IsTaskCommentAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user