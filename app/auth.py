from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from app.models import Token

class TokenTeamsAuthentication(TokenAuthentication):

    def get_token_from_auth_header(self, auth):
        auth = auth.split()
        if not auth or (auth[0].lower() != b'bearer'):
            return None

        if len(auth) == 1:
            raise AuthenticationFailed('Invalid token header. No credentials provided.')
        elif len(auth) > 2:
            raise AuthenticationFailed('Invalid token header. Token string should not contain spaces.')

        try:
            return auth[1].decode()
        except UnicodeError:
            raise AuthenticationFailed('Invalid token header. Token string should not contain invalid characters.')

    def authenticate(self, request):
        auth = get_authorization_header(request)
        key = self.get_token_from_auth_header(auth)

        if key:
            return self.authenticate_credentials(key)

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')

        if not token.is_active:
            raise AuthenticationFailed(key_type.capitalize() + ' inactive or deleted.')

        user = token.owner
        return (user, token)
