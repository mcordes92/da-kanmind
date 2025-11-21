from django.contrib.auth.models import User
from django.db import models


class Boards(models.Model):
    """Model representing a Kanban board with owner and members."""

    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_boards")
    members = models.ManyToManyField(User, related_name="member_boards", blank=True)

    def __str__(self):
        return self.title