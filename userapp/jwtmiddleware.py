
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.http import JsonResponse

class CustomJWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip JWT middleware check for the login endpoint
        # print('JJJJJJJJJJJJJJWWWWWWWWWWWWWTTTTTTTTTTTTTT')
        if request.path != '/userapp/api/login/':
            # print('inside  JJJJJJJJJJJJJJWWWWWWWWWWWWWTTTTTTTTTTTTTT')
            jwt_auth = JWTAuthentication()
            try:
                authentication_tuple = jwt_auth.authenticate(request)
                
                if authentication_tuple:
                    user, validated_token = authentication_tuple

                    if user:
                        request.user = user

            except (InvalidToken, TokenError):
                # Handle token errors
                return JsonResponse({'error': 'Invalid or expired token'}, status=401)
                
        response = self.get_response(request)
        # print(response, 'wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        return response
