from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'  # Serialize all fields of the model

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    email = serializers.EmailField(
        required=True,
        error_messages={
            'unique': _('Já existe uma conta com este email.'),
            'required': _('Email é obrigatório.'),
            'blank': _('Email não pode estar vazio.')
        }
    )

    class Meta:
        model = User
        fields = ('email', 'password', 'password2')

    def validate_email(self, value):
        """Check that the email is not already in use."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Já existe uma conta com este email.")
        return value

    def validate(self, data):
        # Ensure the passwords match
        if data['password'] != data['password2']:
            raise serializers.ValidationError("As senhas não coincidem.")
        return data

    def create(self, validated_data):
        # Remove password confirmation field from validated data
        validated_data.pop('password2')
        # Create the user using the custom manager
        user = User.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        """Customize the serialized output."""
        data = super().to_representation(instance)
        return data
    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("The new passwords do not match.")
        return data

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    test = serializers.BooleanField(default=False)

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("There is no user registered with this email address.")
        return value

from .tokens import password_reset_token
from django.utils.http import urlsafe_base64_decode

class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user.")
        
        if not password_reset_token.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")
        
        return data

    def save(self):
        uid = urlsafe_base64_decode(self.validated_data['uid']).decode()
        user = User.objects.get(pk=uid)
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.translation import gettext_lazy as _

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     email = serializers.EmailField(
#         required=True,
#         error_messages={
#             'required': _('Email é obrigatório.'),
#             'blank': _('Email não pode estar vazio.')
#         }
#     )
#     password = serializers.CharField(
#         write_only=True,
#         required=True,
#         error_messages={
#             'required': _('Senha é obrigatória.'),
#             'blank': _('A senha campo não pode estar vazio.')
#         }
#     )

#     default_error_messages = {
#         'no_active_account': _('Nenhuma conta ativa encontrada com as credenciais fornecidas.')
#     }

#     def validate(self, attrs):
#         # Call the superclass validate method
#         data = super().validate(attrs)
#         return data

from rest_framework.exceptions import ValidationError

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # Ensure email is used as the username field

    email = serializers.EmailField(
        required=True,
        error_messages={
            'required': _('Email é obrigatório.'),
            'blank': _('Email não pode estar vazio.')
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={
            'required': _('Senha é obrigatória.'),
            'blank': _('A senha campo não pode estar vazio.')
        }
    )

    default_error_messages = {
        'no_active_account': _('Nenhuma conta ativa encontrada com as credenciais fornecidas.')
    }

    def validate(self, attrs):
        # Call the parent class's validate method
        data = super().validate(attrs)

        # If validation fails (no active account or incorrect credentials)
        if not data:
            raise ValidationError({"message": self.error_messages['no_active_account']})

        return data