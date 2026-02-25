from rest_framework_simplejwt.authentication import JWTAuthentication

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that reads the access token from a cookie named 'access_token'.
    """
    def authenticate(self, request):
        # Token aus Cookies holen
        access_token = request.COOKIES.get('access_token')

        if access_token:
            # Setzt den Authorization Header, damit die Base-Klasse ihn erkennt
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        # Aufruf der Standard-Authentifizierung
        return super().authenticate(request)