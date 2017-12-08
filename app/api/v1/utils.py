from rest_framework import status
from rest_framework.response import Response
from app.models import *
from django.contrib.auth import get_user_model
User = get_user_model()

def getUserByEmail(_email):
    try:
        return User.objects.get(email=_email)
    except User.DoesNotExist:
        return None

def getTask(_taskId):
    try:
        return Task.objects.get(id=_taskId)
    except Task.DoesNotExist:
        return None

def getJob(_jobId):
    try:
        return Job.objects.get(id=_jobId)
    except Job.DoesNotExist:
        return None

def getUser(_userId):
    try:
        return User.objects.get(id=_userId)
    except User.DoesNotExist:
        return None

def getProjectByOwner(_userId):
    try:
        return Project.objects.get(owner_id=_userId)
    except Project.DoesNotExist:
        return None

def isProjectOwner(_userId, _projectId):
    try:
        return Project.objects.get(owner_id=_userId, id=_projectId)
    except Project.DoesNotExist:
        return None

def isJobAssigned(_userId, _jobId):
    try:
        return JobUsers.objects.get(user_id=_userId, job_id=_jobId)
    except JobUsers.DoesNotExist:
        return None

def isTaskAssigned(_userId, _userTaskId):
    try:
        return UserTask.objects.get(user_id=_userId, id=_userTaskId)
    except UserTask.DoesNotExist:
        return None

def isAssignedTask(_userId, _userTaskId):
    try:
        return UserTask.objects.get(user_id=_userId, task_id=_userTaskId)
    except UserTask.DoesNotExist:
        return None

def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def errorResponse(_message):
    data = {
        "success": False,
        "message": _message
    }
    return Response(
        data,
        status=status.HTTP_400_BAD_REQUEST,
    )
