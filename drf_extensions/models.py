import datetime

from django.conf import settings
from django.utils import timezone

from rest_framework.authtoken.models import Token


class ExpirationToken(Token):

    @property
    def expired_at(self):
        time_delta = datetime.timedelta(seconds=settings.AUTH_TOKEN_EXPIRED_IN)
        return self.created + time_delta

    @property
    def expired(self):
        if settings.DEBUG:
            return False
        return self.expired_at < timezone.now()

    class Meta(Token.Meta):
        abstract = False
