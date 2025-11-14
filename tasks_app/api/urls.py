from django.urls import path, include
from rest_framework_nested import routers
from .views import TaskViewSet, TaskCommentViewSet, TaskAssignedOrReviewingSet

router = routers.SimpleRouter()
router.register(r'tasks', TaskViewSet)

comments_router = routers.NestedSimpleRouter(router, r'tasks', lookup='task')
comments_router.register(r'comments', TaskCommentViewSet, basename='task-comments')

urlpatterns = [
    path('tasks/assigned-to-me/', TaskAssignedOrReviewingSet.as_view({"get": "list"}, mode="assigned-to-me"), name='tasks-assigned-to-me'),
    path('tasks/reviewing/', TaskAssignedOrReviewingSet.as_view({"get": "list"}, mode="reviewing"), name='tasks-reviewing'),
    path(r'', include(router.urls)),
    path(r'', include(comments_router.urls)),
]