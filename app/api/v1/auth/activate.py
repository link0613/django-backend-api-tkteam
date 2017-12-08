from django.db import IntegrityError, transaction
from django.conf import settings as django_settings
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers, exceptions
from app.models import Token

from . import constants, utils
from django.contrib.auth import authenticate, get_user_model

from rest_framework import generics, permissions, status
from rest_framework.response import Response

User = get_user_model()

class UidAndTokenSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    default_error_messages = {
        'invalid_token': constants.INVALID_TOKEN_ERROR,
        'invalid_uid': constants.INVALID_UID_ERROR,
    }

    def validate_uid(self, value):
        try:
            uid = utils.decode_uid(value)
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError) as error:
            raise serializers.ValidationError(self.error_messages['invalid_uid'])
        return value

    def validate(self, attrs):
        attrs = super(UidAndTokenSerializer, self).validate(attrs)
        if not self.context['view'].token_generator.check_token(self.user, attrs['token']):
            raise serializers.ValidationError(self.error_messages['invalid_token'])
        return attrs


class ActivationSerializer(UidAndTokenSerializer):
    default_error_messages = {
        'stale_token': constants.STALE_TOKEN_ERROR,
    }

    def validate(self, attrs):
        attrs = super(ActivationSerializer, self).validate(attrs)
        if self.user.is_active:
            raise exceptions.PermissionDenied(self.error_messages['stale_token'])
        return attrs

class ActivationView(utils.ActionViewMixin, generics.GenericAPIView):
    """
    Use this endpoint to activate user account.
    """
    serializer_class = ActivationSerializer
    permission_classes = (
        permissions.AllowAny,
    )
    token_generator = default_token_generator

    def _action(self, serializer):
        serializer.user.is_active = True
        serializer.user.save()

        if django_settings.AUTH.get('SEND_CONFIRMATION_EMAIL'):
            email_factory = utils.UserConfirmationEmailFactory.from_request(
                self.request, user=serializer.user)
            email = email_factory.create()
            email.send()
        data = {
            "success": True,
            "message": "Account activated."
        }
        return Response(data=data, status=status.HTTP_200_OK)
