from django.db import models
import uuid
from django.conf import settings

class UserTask(models.Model):
    id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    date = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True)
    is_disabled = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    task = models.ForeignKey(
        'Task',
        related_name="task_data",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="task_user",
        on_delete=models.CASCADE
    )
