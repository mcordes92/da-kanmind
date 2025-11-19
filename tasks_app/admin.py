from django.contrib import admin
from .models import Tasks, TaskComments

# Register your models here.
admin.site.register(Tasks)
admin.site.register(TaskComments)