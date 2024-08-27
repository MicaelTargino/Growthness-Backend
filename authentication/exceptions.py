from rest_framework.views import exception_handler
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler to format error responses.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the custom error message formatting for authentication errors.
    if isinstance(exc, AuthenticationFailed):
        # Customize the response for AuthenticationFailed exceptions
        response = Response(
            {"message": str(exc.detail)},
            status=status.HTTP_401_UNAUTHORIZED
        )

    return response
