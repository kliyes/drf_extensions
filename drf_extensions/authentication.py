from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import TokenAuthentication, \
    get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import SAFE_METHODS

from .models import ExpirationToken


class ExpirationTokenAuthentication(TokenAuthentication):
    model = ExpirationToken

    def authenticate(self, request):
        auth = super(ExpirationTokenAuthentication, self).authenticate(request)
        if auth is None:
            keyword = self.keyword.lower()
            token = request.GET.get(keyword) or request.POST.get(keyword)
            if not token:
                raise AuthenticationFailed(_(
                    "Add keyword `%s` before token key, "
                    "or include it into GET/POST query parameter") % keyword)
            return self.authenticate_credentials(token)
        return auth

    def authenticate_credentials(self, key):
        user, token = super(ExpirationTokenAuthentication, self)\
            .authenticate_credentials(key)
        if token.expired:
            raise AuthenticationFailed(_("Login expired"))
        return user, token


class AnonymousUserSafeAuthentication(ExpirationTokenAuthentication):
    """
    Do not authenticate if request is safe methods
    """
    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        # do authentication if token given or request method is not SAFE methods
        if auth or request.method not in SAFE_METHODS:
            return super(AnonymousUserSafeAuthentication, self).authenticate(
                request
            )
