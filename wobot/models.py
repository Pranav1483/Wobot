from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(null=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)