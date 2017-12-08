from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from django.db import IntegrityError, transaction
from django.conf import settings as django_settings

from rest_framework import serializers
from app.models import Token, Project
from app.serializers import UserDetailSerializer
from rest_framework.views import APIView

from ..utils import *
from . import constants, utils

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True,
        validators=django_settings.AUTH.get('PASSWORD_VALIDATORS')
    )
    confirm_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        required=True,
        validators=django_settings.AUTH.get('PASSWORD_VALIDATORS')
    )
    company_name = serializers.CharField(
        write_only=True,
        required=True
    )

    default_error_messages = {
        'cannot_create_user': constants.CANNOT_CREATE_USER_ERROR,
    }

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD, User._meta.pk.name, 'password', 'confirm_password', 'referrer', 'is_project_owner', 'company_name'
        )

    def create(self, validated_data):
        try:
            validated_data.pop('confirm_password')
            validated_data.pop('company_name')
            user = self.perform_create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                self.error_messages['cannot_create_user']
            )

        return user

    def perform_create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            if django_settings.AUTH.get('SEND_ACTIVATION_EMAIL'):
                user.is_active = False
                user.save(update_fields=['is_active'])

        return user

class RegistrationView(APIView):
    """
    Use this endpoint to register new user.
    """
    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request):
        data = request.data

        if request.data.get("referrer", None) == None:
            data['referrer'] = None
        if (request.data.get("is_project_owner", None) == None or request.data.get("is_project_owner") == False) and (request.data.get("company_name", None) == None or request.data.get("company_name").strip() == ''):
            data['company_name'] = 'NULL'

        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            if request.data.get('confirm_password', None) == None or ( request.data['confirm_password'] != request.data['password'] ):
                return errorResponse("Please confirm password")
            else:
                user = serializer.save()
                try:
                    if django_settings.AUTH.get('SEND_ACTIVATION_EMAIL'):
                        self.send_activation_email(user)
                    elif django_settings.AUTH.get('SEND_CONFIRMATION_EMAIL'):
                        self.send_confirmation_email(user)
                except:
                    import pprint
                    pprint.pprint('error in sending email')

                if request.data.get("is_project_owner", None):
                    Project.objects.create(owner_id=user.id, name=request.data['company_name'])

                return Response({
                    "success": True,
                    "message": "Registration successful. Please check email for activation link."
                }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "message": "Errors while registering data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    def send_activation_email(self, user):
        email_factory = utils.UserActivationEmailFactory.from_request(
            self.request, user=user
        )
        email = email_factory.create()
        email.send()

    def send_confirmation_email(self, user):
        email_factory = utils.UserConfirmationEmailFactory.from_request(
            self.request, user=user
        )
        email = email_factory.create()
        email.send()
