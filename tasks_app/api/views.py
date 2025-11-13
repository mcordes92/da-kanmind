from rest_framework import viewsets, views, mixins
from rest_framework.permissions import IsAuthenticated
from tasks_app.models import Tasks
from .serializers import TaskSerializer
from .permissions import IsBoardMember, IsTaskOwner, IsBoardOwner

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

class TaskCommentViewSet(viewsets.ModelViewSet):
    pass