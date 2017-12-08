from django.db import models
from rest_framework import serializers
import uuid
from django.conf import settings

class Job(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(null=True, max_length=255)
    description = models.TextField(null=True, max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    rate = models.FloatField()
    project = models.ForeignKey(
        'Project',
        related_name="project_data",
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ('date',)
