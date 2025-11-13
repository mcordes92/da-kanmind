from rest_framework.permissions import BasePermission
from boards_app.models import Boards
from tasks_app.models import Tasks

class IsBoardOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.board.owner == request.user

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
    
class IsTaskOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.assignee_id == request.user