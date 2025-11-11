from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardsViewSet

router = DefaultRouter()
router.register(r'boards', BoardsViewSet, basename='board')

urlpatterns = [
    path('', include(router.urls)),
]