from django.urls import path

from .views import RegistrationView, LoginView

# URL patterns for user authentication endpoints
urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
]
