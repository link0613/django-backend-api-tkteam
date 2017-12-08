
from app.serializers import NewJobUserSerializer, JobUsersListSerializer, NewJobSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from ..utils import *
from app.models import JobUsers

class FreelancersList(APIView):
    """
    List all users assigned to job, or assign new user to job
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, jobId, format=None):

        job = getJob(jobId)
        if not job:
            return errorResponse("Job not available.")

        job_users = JobUsers.objects.filter(job_id=jobId)
        serializer = JobUsersListSerializer(job_users, many=True)
        job_serializer = NewJobSerializer(job)

        return Response({
            "freelancers": serializer.data,
            "job": job_serializer.data
        })

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

    def post(self, request, jobId, format=None):
        self.validateJob(request, jobId)
        user = getUserByEmail(request.data['email'])
        if not getJob(jobId):
            return errorResponse("Job not available.")
        if request.data.get('email', None) == None or not user:
            return errorResponse("Freelancer not found.")

        data = {}
        data['job'] = jobId
        data['user'] = user.id
        serializer = NewJobUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data, 'result': { 'message': 'Job was assigned to freelancer successfully.' } }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
