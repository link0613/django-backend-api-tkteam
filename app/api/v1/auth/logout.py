from . import utils
from django.contrib.auth import authenticate, get_user_model

from rest_framework import permissions, views, status
from rest_framework.response import Response


class LogoutView(views.APIView):
    """
    Use this endpoint to logout user (remove user authentication token).
    """
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        utils.logout_user(request)
        data = {
            'success': True
        }
        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )
