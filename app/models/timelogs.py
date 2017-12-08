from django.db import models
from rest_framework import serializers
import uuid
from django.conf import settings

class TimeLogs(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    description = models.TextField(blank=True, null=True, max_length=255)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    task = models.ForeignKey(
        'UserTask',
        related_name="user_task_data",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    class Meta:
        ordering = ('start_date',)
