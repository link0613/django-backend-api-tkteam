from rest_framework import serializers
from app.models import *

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'is_admin', 'avatar', 'is_project_owner')

class NewJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ('id', 'name', 'description', 'date', 'rate', 'project')

class TaskJobSerializer(serializers.ModelSerializer):
    job = NewJobSerializer()
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'job')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'date', 'owner')

class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'date', 'owner')

class UserTaskDetailSerializer(serializers.ModelSerializer):
    task = TaskJobSerializer()
    class Meta:
        model = UserTask
        fields = ('id', 'date', 'is_disabled', 'is_completed', 'task')

class NewTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'job')

class NewUserTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTask
        fields = ('id', 'date', 'task', 'user', 'is_completed', 'is_disabled', 'date_completed')

class TaskSerializer(serializers.ModelSerializer):
    #users = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'job', 'status')

    def get_users(self, obj):
        return UserTask.objects.filter(task_id=obj.id)

    def get_status(self, obj):
        stat = 'Pending'
        users = self.get_users(obj)
        if len(users) > 0:
            stat = 'Completed' if users[0].is_completed else 'On Progress'

        return stat

class JobSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    job_tasks = TaskSerializer(many=True)
    class Meta:
        model = Job
        fields = ('id', 'name', 'description', 'date', 'rate', 'project', 'job_tasks')

class TaskDetailSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'start_date', 'end_date', 'job')

class JobUsersListSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()
    class Meta:
        model = JobUsers
        fields = ('id', 'date', 'user', 'job')

class JobUsersSerializer(serializers.ModelSerializer):
    job = JobSerializer()
    user = UserDetailSerializer()
    class Meta:
        model = JobUsers
        fields = ('id', 'date', 'user', 'job')

class NewJobUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobUsers
        fields = ('id', 'date', 'job', 'user')

class TimeLogsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLogs
        fields = ('id', 'description', 'task', 'start_date', 'end_date')

class TimeLogMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeLogMedia
        fields = ('id', 'image', 'date', 'timelog')

class TimeLogsListSerializer(serializers.ModelSerializer):
    timelog_data = TimeLogMediaSerializer(many=True)
    task = UserTaskDetailSerializer()

    class Meta:
        model = TimeLogs
        fields = ('id', 'description', 'task', 'start_date', 'end_date', 'timelog_data')
