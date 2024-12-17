from rest_framework import permissions
from .models import ObjectPermission
from .constants import ActionEnum


class HasObjectPermission(permissions.BasePermission):
    """
    Custom permission to check if a user has permission for a specific action
    using predefined ActionEnum values.
    """

    ACTION_MAP = {
        "list": ActionEnum.VIEW.value,
        "retrieve": ActionEnum.VIEW.value,
        "create": ActionEnum.CREATE.value,
        "update": ActionEnum.EDIT.value,
        "partial_update": ActionEnum.EDIT.value,
        "destroy": ActionEnum.DELETE.value,
    }

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has global 'create' permission (so null object_id) for creation actions.
        """
        if not request.user.is_authenticated:
            return False

        action = self.ACTION_MAP.get(view.action)
        if action == ActionEnum.CREATE.value:
            # Check if the user has global CREATE permission
            return ObjectPermission.objects.filter(
                user=request.user,
                action=ActionEnum.CREATE.value,
                object_id__isnull=True
            ).exists()

        return True

    def has_object_permission(self, request, view, obj):
        """
        Check object-level permission using ActionEnum values.
        """
        # Map DRF view action to ActionEnum
        action = self.ACTION_MAP.get(view.action)
        
        if not action:
            # Deny permission if the action is not mapped
            return False

        return ObjectPermission.objects.filter(
            user=request.user,
            action=action,
            object_id=obj.id
        ).exists()
