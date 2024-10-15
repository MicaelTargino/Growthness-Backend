from .models import User 
from django.core.exceptions import ObjectDoesNotExist

def authenticate_or_create_user_from_google_idinfo(idinfo):
    """
    Authenticate or create a user based on Google ID token information.
    `idinfo` is the decoded Google ID token containing user information.
    """
    try:
        # Try to find an existing user by their Google email address
        user = User.objects.get(email=idinfo['email'])
    except ObjectDoesNotExist:
        # If the user doesn't exist, create a new one
        user = User.objects.create_user(
            email=idinfo['email'],
            first_name=idinfo.get('given_name', ''),
            last_name=idinfo.get('family_name', ''),
            password=None  # Set password to None, as this user will log in via Google only
        )

    return user