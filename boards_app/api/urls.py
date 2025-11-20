from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import BoardsViewSet, EmailCheck

# Register board viewset with router for RESTful endpoints
router = DefaultRouter()
router.register(r'boards', BoardsViewSet, basename='board')

# URL patterns for boards and email validation endpoints
urlpatterns = [
    path('email-check/', EmailCheck.as_view(), name='email-check'),
    path('', include(router.urls)),
]