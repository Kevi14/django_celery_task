from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid
from .constants import ActionEnum

class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email



class ObjectPermission(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="permissions")
    action = models.CharField(max_length=20, choices=ActionEnum.choices())
    object_id = models.UUIDField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'action', 'object_id')

    def __init__(self, *args, permissions=None, **kwargs):
        """
        Initialize ObjectPermission with a list of actions (optional shortcut).
        permissions: List of actions from Action Enum, e.g., [Action.VIEW, Action.EDIT]
        """
        super().__init__(*args, **kwargs)
        if permissions:
            self.action = [action.value for action in permissions]

    def __str__(self):
        return f"{self.user.email} - {self.action} for Object ({self.object_id})"