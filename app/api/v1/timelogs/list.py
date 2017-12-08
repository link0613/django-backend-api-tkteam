
from app.serializers import TimeLogsListSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..utils import errorResponse, getUser
import datetime
from app.models import TimeLogs
from django.db import connection

class TimeLogsList(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, userId, format=None):
        user = getUser(userId)
        if not user:
            return errorResponse('User not found.')
        else:
            time_logs = TimeLogs.objects.filter(task__user=user)
            serializer = TimeLogsListSerializer(time_logs, many=True)
            return Response(serializer.data)
