from .models import User
from django.conf import settings
from rest_framework import status
from django.core.mail import send_mail
from rest_framework.views import APIView
from .tokens import password_reset_token
from rest_framework.response import Response
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_password_reset_email
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    UserRegistrationSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
    CustomTokenObtainPairSerializer
)

# ---- Example of protected CBV and FBV views ----- 

class ProtectedView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response({'message': 'This is a protected view!'})

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def protected_view(request):
#     return Response({'message': 'This is a protected view!'})

class UserRegistrationView(APIView):
    """ User Registration
    
    Body: {
        'username': str,
        'email': str',
        'password': str,
        'password2': str
    }

    Returns: 201 | 400 
    """
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        
        # Extract the first error message
        first_error = next(iter(serializer.errors.values()))[0]
        return Response({"message": str(first_error)}, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(TokenObtainPairView):
    """
    Custom Token Obtain Pair View that returns only the first error message.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        # Call .is_valid() without raising an exception
        if serializer.is_valid():
            # If valid, return the standard response
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        else:
            # If not valid, format and return the first error message
            first_error = next(iter(serializer.errors.values()))[0]
            return Response({"message": str(first_error)}, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    """ User Log Out 

    Authorization Header: {
        'AUTHORIZATION': 'Bearer {access_token}'
    }
    
    Body: {
        'refresh_token': str
    }

    Returns: 205 | 400 | 401
    """


    permission_classes = (IsAuthenticated,) # Need to send access token in Authorization header

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token) # validate and parse the token 
            token.blacklist() # blacklist the refresh token

            return Response(status=status.HTTP_205_RESET_CONTENT) # Successfully Logged out
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST) # Not valid refresh token
        
class ChangePasswordView(APIView):
    """ User Change Password 

    Authorization Header: {
        'AUTHORIZATION': 'Bearer {access_token}'
    }
    
    Body: {
        'old_password': str,
        'new_password': str,
        'confirm_password': str
    }

    Returns: 200 | 400 | 401
    """

    permission_classes = (IsAuthenticated,) # Need to send access token in Authorization header

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordResetRequestView(APIView):
    """ User request password recovery link 
    
    Body: {
        'email': str
    }

    Returns: 200 | 400 
    """
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            test = serializer.validated_data.get('test', False)
            user = User.objects.get(email=email)
            token = password_reset_token.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            if not test:
                send_password_reset_email.delay(email, reset_url)
            return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    """ User request password update via recovery link
    
    Body: {
        'new_password': str,
        'confirm_password': str,
        'uid': str,
        'token': str
    }

    Returns: 200 | 400 
    """
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
