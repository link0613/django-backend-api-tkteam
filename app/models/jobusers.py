from django.db import models
import uuid
from django.conf import settings

class JobUsers(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    job = models.ForeignKey(
        'Job',
        related_name="job_data",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="job_user",
        on_delete=models.CASCADE
    )
