from rest_framework import serializers
from accounts import serializers as account_serializers
from projects import models as project_models
from accounts import models as account_models


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Task
        fields = ('id', 'creator', 'title', 'description', 'status',
                  'project', 'assignee', 'created_at', 'updated_at')
        read_only_fields = ('creator',)

    def validate_assignee(self, value):
        creator: account_models.User = self.context['request'].user
        assignee: account_models.User = value
        if creator.is_developer and assignee != creator:
            raise serializers.ValidationError(
                'You can only assign tasks to yourself.')
        elif creator.is_project_manager and not assignee.is_developer:
            raise serializers.ValidationError(
                'You can only assign tasks to developers.')
        return value

    def validate_project(self, value):
        project: project_models.Project = value
        creator: account_models.User = self.context['request'].user
        if creator.is_project_manager and project.creator != creator:
            raise serializers.ValidationError(
                'You can only assign tasks to projects you have created.')
        elif creator.is_developer and not project.has_assignee(creator):
            raise serializers.ValidationError(
                'You can only assign tasks to projects you have been assigned to.')
        return value

    def validate(self, attrs):
        project: project_models.Project = attrs.get('project')
        assignee: account_models.User = attrs.get('assignee')
        if not project.has_assignee(assignee):
            raise serializers.ValidationError(
                'Task assignee must be in the project.')
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create({**validated_data, 'creator': self.context['request'].user})


class TaskUpdateSerializer(TaskCreateSerializer):
    class Meta:
        model = project_models.Task
        fields = ('id', 'creator', 'title', 'description', 'status',
                  'project', 'assignee', 'created_at', 'updated_at')
        read_only_fields = ('creator', 'project')

    def validate_project(self, value):
        return value


class TaskListRetrieveSerializer(serializers.ModelSerializer):
    assignee = account_serializers.UserSerializer(many=False, read_only=True)
    creator = account_serializers.UserSerializer(many=False, read_only=True)

    class Meta:
        model = project_models.Task
        fields = ('id', 'creator', 'title', 'description', 'status',
                  'project', 'assignee', 'created_at', 'updated_at')


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Project
        fields = ('id', 'title', 'description', 'tasks',
                  'creator', 'assignees', 'created_at', 'updated_at')
        extra_kwargs = {'assignees': {'required': False}}
        read_only_fields = ('creator', 'tasks')

    def validate_assignees(self, value):
        user_list: list[account_models.User] = value
        for user in user_list:
            if not user.is_developer:
                raise serializers.ValidationError(
                    'All assignees must be developers.')
        return value

    def create(self, validated_data):
        return super().create({**validated_data, 'creator': self.context['request'].user})


class ProjectListRetrieveSerializer(serializers.ModelSerializer):
    assignees = account_serializers.UserSerializer(many=True, read_only=True)
    creator = account_serializers.UserSerializer(many=False, read_only=True)
    tasks = TaskListRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = project_models.Project
        fields = ('id', 'title', 'description', 'tasks',
                  'creator', 'assignees', 'created_at', 'updated_at')
