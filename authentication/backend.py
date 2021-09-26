import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        # `auth_header` should be an array with two elements: 1) the name of
        # the authentication header (in this case, "Bearer") and 2) the JWT 
        # token that we should authenticate against.
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            # Invalid token header.
            return None

        elif len(auth_header) > 2:
            # Invalid token header. 
            return None
        
        #decoding the JWT token if its valid token
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            #if prefix of token is not valid we dont authenticate
            return None

        #authenticating token and user using self defined function
        return self._authenticate_credentials(request, token)

    def _authenticate_credentials(self, request, token):
        """
        this function authenticate token and return user and token as object
        """
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except:
            msg = 'Authentivation token not valid'
            raise exceptions.AuthenticationFailed(msg)
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            msg = 'User does not exist'
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = 'inactive user token'
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)