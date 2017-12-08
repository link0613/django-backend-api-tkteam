from django.db import IntegrityError, transaction

from rest_framework import serializers
from app.models import Token
from app.serializers import UserDetailSerializer
from ..utils import *
from . import constants, utils
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView

from rest_framework import generics, permissions, status
from rest_framework.response import Response

User = get_user_model()

class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = (
            'auth_token',
        )

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True, style={'input_type': 'password'}
    )

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields[User.USERNAME_FIELD] = serializers.CharField(required=True)

class LoginView(APIView):
    """
    Use this endpoint to obtain user authentication token.
    """
    permission_classes = (
        permissions.AllowAny,
    )

    def post(self, request):
        user = getUserByEmail(request.data.get('email', None))
        if user and not user.is_active:
            return errorResponse(constants.INACTIVE_ACCOUNT_ERROR)

        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.data.get('email'),
                password=serializer.data.get('password')
            )
            if user:
                token = utils.login_user(request, user)
                data = {
                    'token': TokenSerializer(token).data,
                    'user': UserDetailSerializer(user).data
                }

                return Response(
                    data=data,
                    status=status.HTTP_200_OK,
                )
            else:
                return errorResponse(constants.INVALID_CREDENTIALS_ERROR)
        return Response({
            "success": False,
            "message": "All fields are required.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
