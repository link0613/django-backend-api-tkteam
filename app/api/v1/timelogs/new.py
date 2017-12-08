
from app.serializers import TimeLogsSerializer, NewUserTaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..utils import *
import datetime
from app.models import TimeLogs, UserTask

class NewTimeLog(APIView):
    """
    List all time of users for a project, or create a new user time log for a project.
    """

    permission_classes = (permissions.IsAuthenticated,)

    # def get(self, request, format=None):
    #     projects = UserProject.objects.filter(user=request.user)
    #     serializer = UserProjectSerializer(projects, many=True)
    #     return Response(serializer.data)

    def post(self, request, jobId, taskId, action, format=None):
        if not isJobAssigned(request.user.id, jobId):
            return errorResponse('Job not accessible.')
        else:
            if action == 'start':
                new_usertask_data = {}
                new_usertask_data['user'] = request.user.id
                new_usertask_data['task'] = taskId

                usertask = isAssignedTask(request.user.id, taskId)
                if usertask:
                    userTaskId = usertask.id
                else:
                    new_usertask_serializer = NewUserTaskSerializer(data=new_usertask_data)
                    if new_usertask_serializer.is_valid():
                        new_usertask_serializer.save()
                        userTaskId = new_usertask_serializer.data['id']

                data = request.data
                data['task'] = userTaskId
                data['start_date'] = datetime.datetime.now()
                serializer = TimeLogsSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()

                    return Response({'data': serializer.data, 'result': { 'message': 'Time log was saved successfully.' } }, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            if action == 'complete':
                usertask = isAssignedTask(request.user.id, taskId)
                usertask.is_completed = True
                usertask.date_completed = datetime.datetime.now()
                usertask.save()
                action = 'stop'

            if action == 'stop':
                usertask = isAssignedTask(request.user.id, taskId)
                timelog = TimeLogs.objects.get(task_id=usertask.id, id=request.data['id'])
                if timelog:
                    timelog.end_date = datetime.datetime.now()
                    timelog.save()
                return Response({'result': { 'message': 'Time log was saved successfully.' } }, status=status.HTTP_201_CREATED)
