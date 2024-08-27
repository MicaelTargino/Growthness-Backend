from django.urls import path 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserLogoutView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    ProtectedView
)

urlpatterns = [
    path('protected-endpoint', ProtectedView.as_view(), name="protected-endpoint"),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('token/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # body: {'refresh': str}, response: {'access': str}
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), 
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
