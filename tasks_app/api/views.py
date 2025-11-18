from django.shortcuts import get_object_or_404
from rest_framework import viewsets, views, mixins, status
from rest_framework.permissions import IsAuthenticated
from tasks_app.models import Tasks, TaskComments
from .serializers import TaskSerializer, TaskCommentSerializer
from .permissions import IsBoardMember, IsTaskOwner, IsBoardOwner, IsTaskCommentAuthor
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class TaskViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    lookup_field = "pk"

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [ IsAuthenticated, IsBoardMember ]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [ IsAuthenticated, IsBoardMember ]
        elif self.action == 'destroy':
            permission_classes = [ IsAuthenticated, (IsTaskOwner | IsBoardOwner) ]
        else:
            permission_classes = [ IsAuthenticated ]
        return [permission() for permission in permission_classes]
    
    def partial_update(self, request, *args, **kwargs):
        response = super().partial_update(request, *args, **kwargs)

        if isinstance(response.data, dict) and 'comments_count' in response.data:
            response.data.pop('comments_count')
            
        return response

class TaskCommentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = TaskComments.objects.all()
    permission_classes = [ IsAuthenticated ]
    serializer_class = TaskCommentSerializer
    lookup_field = "pk"

    def get_queryset(self):
        task_id = self.kwargs.get('task_pk')
        task = get_object_or_404(Tasks.objects.select_related('board'), pk=task_id)
        user = self.request.user
        board = task.board

        if user != board.owner and not user in board.members.all():
            raise PermissionDenied("You do not have permission to view comments for this task.")
                
        return TaskComments.objects.filter(task_id=task_id).select_related('author')
    
    def create(self, request, *args, **kwargs):
        task_id = kwargs.get('task_pk')
        task = get_object_or_404(Tasks.objects.select_related('board'), pk=task_id)
        user = request.user
        board = task.board

        if user != board.owner and not user in board.members.all():
            raise PermissionDenied("You do not have permission to add comments to this task.")
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(author=user, task=task)

        response = {
            "id": serializer.instance.id,
            "created_at": serializer.instance.created_at,
            "author": user.profile.full_name,
            "content": serializer.instance.content
        }

        return Response(response, status=201)
    
    def destroy(self, request, *args, **kwargs):
        task_id = kwargs.get('task_pk')
        comment_id = kwargs.get('pk')
        
        comment = get_object_or_404(TaskComments.objects.select_related('author', 'task'), pk=comment_id, task_id=task_id)

        if self.request.user != comment.author:
            raise PermissionDenied("You do not have permission to delete this comment.")
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskAssignedOrReviewingSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    mode = None

    def get_dispatch(self, request, *args, **kwargs):
        if "mode" in kwargs:
            self.mode = kwargs.pop("mode")
        return super().get_dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        qs = Tasks.objects.all()
        if self.mode == "assigned-to-me":
            qs = qs.filter(assignee=self.request.user)
        elif self.mode == "reviewing":
            qs = qs.filter(reviewer=self.request.user)
        return qs