from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BoardsViewSet, EmailCheck

router = DefaultRouter()
router.register(r'boards', BoardsViewSet, basename='board')

urlpatterns = [
    path('email-check/', EmailCheck.as_view(), name='email-check'),
    path('', include(router.urls)),
]