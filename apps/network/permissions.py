import logging

from rest_framework.permissions import BasePermission

logger = logging.getLogger(__name__)


class IsActiveEmployee(BasePermission):
    """Grant access only to active users that are registered as employees."""

    message = "Access is allowed only for active employees."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            logger.debug(
                "Permission denied: unauthenticated request to %s %s",
                request.method,
                request.path,
            )
            return False

        if not request.user.is_active:
            logger.warning(
                "Permission denied: inactive user '%s' attempted %s %s",
                request.user.username,
                request.method,
                request.path,
            )
            return False

        if not hasattr(request.user, "employee"):
            logger.warning(
                "Permission denied: user '%s' has no Employee record, attempted %s %s",
                request.user.username,
                request.method,
                request.path,
            )
            return False

        return True
