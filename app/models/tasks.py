from django.db import models
from rest_framework import serializers
import uuid
from django.conf import settings

class Task(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(null=True, max_length=255)
    description = models.TextField(null=True, max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    job = models.ForeignKey(
        'Job',
        related_name="job_tasks",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('start_date',)
