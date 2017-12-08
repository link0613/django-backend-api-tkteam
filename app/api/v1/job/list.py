
from app.serializers import NewJobSerializer, JobSerializer, JobUsersSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from app.models import Job, JobUsers
from ..utils import *

class JobList(APIView):
    """
    List all project jobs, or create a new project job.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        if request.user.is_project_owner:
            project = getProjectByOwner(request.user.id)
            if not project:
                return errorResponse("No project available.")

            jobs = Job.objects.filter(project_id=project.id)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        else:
            user_jobs = JobUsers.objects.filter(user_id=request.user.id)
            serializer = JobUsersSerializer(user_jobs, many=True)
            return Response(serializer.data)


    def post(self, request, format=None):
        project = getProjectByOwner(request.user.id)

        if not project:
            return errorResponse("No project available.")

        data = request.data
        data['project'] = project.id

        serializer = NewJobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'result': { 'message': 'Project job was created successfully.' } }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
