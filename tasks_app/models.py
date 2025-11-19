from django.db import models
from django.contrib.auth.models import User
from boards_app.models import Boards

def choices_status():
    status = ['to-do', 'in-progress', 'review', 'done']
    return status

def choices_priority():
    priority = ['low', 'medium', 'high']
    return priority

class Tasks(models.Model):
    board = models.ForeignKey(Boards, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[(status, status) for status in choices_status()], default='to-do')
    priority = models.CharField(max_length=20, choices=[(priority, priority) for priority in choices_priority()], default='low')
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="review_tasks")
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.board.title}"

class TaskComments(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"Comment by {self.author} on {self.task}"