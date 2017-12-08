
from app.serializers import NewUserTaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..utils import *

class SelectTaskView(APIView):
    """
    User select job task to do
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        jobId = request.data.get('job', None)
        taskId = request.data.get('task', None)

        job = getJob(jobId)
        if not job:
            return errorResponse("Job not available.")

        if not isJobAssigned(request.user.id, jobId):
            return errorResponse("Job not available.")

        task = getJob(taskId)
        if not task:
            return errorResponse("Task not available.")

        if task.job_id != jobId:
            return errorResponse("Task not available.")

        data = {}
        data['task'] = request.data['task']
        data['user'] = request.user.id

        serializer = NewUserTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'result': { 'message': 'Task was selected successfully.' } }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
