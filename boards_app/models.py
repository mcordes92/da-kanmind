from django.db import models
from django.contrib.auth.models import User

"""
Models for the boards application.
"""

class Boards(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_boards")
    members = models.ManyToManyField(User, related_name="member_boards", blank=True)

    def __str__(self):
        return self.title