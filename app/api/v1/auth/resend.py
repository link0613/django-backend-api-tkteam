from rest_framework import permissions
from django.conf import settings as django_settings
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework import status

from ..utils import *
from . import constants, utils

User = get_user_model()

class ResendVerificationView(APIView):
    """
    Use this endpoint to register new user.
    """
    permission_classes = (
        permissions.AllowAny,
    )

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except:
            return None

    def post(self, request):
        if request.data.get('email', None) == None or request.data.get('email', "") == "" :
            return errorResponse('Email is required.')
        user = self.get_user(request.data['email'])
        if not user:
            return errorResponse('Account not found.')

        if user.is_active:
            return errorResponse('Account already active.')

        self.send_activation_email(user)
        data = {
            "success": True,
            "message": "Activation email sent."
        }
        return Response(data=data, status=status.HTTP_200_OK)

    def send_activation_email(self, user):
        email_factory = utils.UserActivationEmailFactory.from_request(
            self.request, user=user
        )
        email = email_factory.create()
        email.send()
