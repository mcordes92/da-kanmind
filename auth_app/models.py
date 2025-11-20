from django.contrib.auth.models import User
from django.db import models

# Extended user profile to store additional user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)