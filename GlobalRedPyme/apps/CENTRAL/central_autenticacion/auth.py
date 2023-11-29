
from rest_framework.authentication import TokenAuthentication
from apps.CENTRAL.central_autenticacion.models import Token
from rest_framework.exceptions import AuthenticationFailed

from datetime import timedelta
from django.utils import timezone
from django.conf import settings



#this return left time
def expires_in(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

    return left_time

# token checker if token expired or not
def is_token_expired(token):
    return expires_in(token) < timedelta(seconds = 0)

# if token is expired new token will be established
# If token is expired then it will be removed
# and new one with different key will be created
def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
    return is_expired

def deleteExpiredTokens():
    expiry_time=timezone.now() -timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS)
    Token.objects.filter(created__lte=expiry_time).delete()
    return True
     

#________________________________________________
#DEFAULT_AUTHENTICATION_CLASSES
class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """
    keyword = settings.TOKEN_KEYWORD
    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key = key)
        except :
            raise AuthenticationFailed("Invalid Token")
        
        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired = token_expire_handler(token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")
        
        return (token.user, token)