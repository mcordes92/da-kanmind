from django.urls import path, include
from rest_framework_nested import routers
from .views import TaskViewSet, TaskCommentViewSet

router = routers.SimpleRouter()
router.register(r'tasks', TaskViewSet)

comments_router = routers.NestedSimpleRouter(router, r'tasks', lookup='task')
comments_router.register(r'comments', TaskCommentViewSet, basename='task-comments')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(comments_router.urls)),
]