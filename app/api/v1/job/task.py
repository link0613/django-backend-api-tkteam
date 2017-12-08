
from app.serializers import TaskSerializer, NewJobSerializer, NewTaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.models import Task
from ..utils import *

class TaskList(APIView):
    """
    List all job tasks, or create a job task.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def validateJob(self, request, jobId):
        project = getProjectByOwner(request.user.id)

        # make sure that a project exist
        if not project:
            return errorResponse("No project available.")

        # make sure that the job is under the project owned by user
        job = getJob(jobId)
        if not job:
            return errorResponse("Job not available.")
        if project.id != job.project_id:
            return errorResponse("Job not available.")

    def get(self, request, jobId, format=None):
        #self.validateJob(request, jobId)

        job = getJob(jobId)
        if not job:
            return errorResponse("Job not available.")

        tasks = Task.objects.filter(job_id=jobId)
        serializer = TaskSerializer(tasks, many=True)
        job_serializer = NewJobSerializer(job)

        return Response({
            "tasks": serializer.data,
            "job": job_serializer.data
        })

    def post(self, request, jobId, format=None):
        self.validateJob(request, jobId)

        data = request.data
        data['job'] = jobId
        serializer = NewTaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'result': { 'message': 'Job task was created successfully.' } }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
