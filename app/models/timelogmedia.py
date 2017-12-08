from django.db import models
from rest_framework import serializers
import uuid

class TimeLogMedia(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    image = models.URLField(blank=True, null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    timelog = models.ForeignKey(
        'TimeLogs',
        related_name="timelog_data",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('date',)
