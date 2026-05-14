import logging

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from django.contrib.auth.models import User

from apps.network.models import OutletAPIKey

logger = logging.getLogger(__name__)


class OutletAPIKeyAuthentication(BaseAuthentication):
    """
    Authenticate requests using a per-outlet secret token.
    Returns only the outlet that owns the key – not the full network list.
    """

    keyword = "X-API-Key"

    def authenticate(self, request: Request) -> tuple[User, str] | None:
        api_key = request.headers.get(self.keyword)
        if not api_key:
            return None

        try:
            outlet_api_key = OutletAPIKey.objects.select_related('user', 'outlet').get(key=api_key)
        except OutletAPIKey.DoesNotExist:
            logger.warning(
                "API key authentication failed: unknown key (prefix='%s...') from %s",
                api_key[:8],
                request.META.get("REMOTE_ADDR"),
            )
            raise AuthenticationFailed("Invalid API key.")

        user = outlet_api_key.user
        outlet = outlet_api_key.outlet
        user._outlet_api_key_outlet = outlet

        logger.debug(
            "API key authentication succeeded: outlet='%s' user='%s' from %s",
            outlet.name,
            user.username,
            request.META.get("REMOTE_ADDR"),
        )

        return (user, api_key)

    def authenticate_header(self, request: Request) -> str:
        return self.keyword
