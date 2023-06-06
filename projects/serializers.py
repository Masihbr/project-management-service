from rest_framework import serializers
from accounts import serializers as account_serializers
from projects import models as project_models
from accounts import models as account_models


class TaskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Task
        fields = ('id', 'title', 'description', 'status',
                  'creator', 'project', 'assignee')
        read_only_fields = ('creator',)

    def validate_assignee(self, value):
        creator = self.context['request'].user
        is_creator_developer = creator.role == account_models.User.Role.DEVELOPER.value
        if is_creator_developer and value != creator:
            raise serializers.ValidationError(
                'You can only assign tasks to yourself.')
        return value

    def validate_project(self, value):
        project: project_models.Project = value
        creator = self.context['request'].user
        is_creator_developer = creator.role == account_models.User.Role.DEVELOPER.value
        is_creator_product_manager = creator.role == account_models.User.Role.PROJECT_MANAGER.value
        if is_creator_product_manager and project.creator != creator:
            raise serializers.ValidationError(
                'You can only assign tasks to your own projects.')
        elif is_creator_developer and not project.assignees.contains(creator):
            raise serializers.ValidationError(
                'You can only assign tasks to your own projects.')
        return value

    def validate(self, attrs):
        project: project_models.Project = attrs.get('project')
        assignee: account_models.User = attrs.get('assignee')
        if not project.assignees.contains(assignee):
            raise serializers.ValidationError(
                'Assignee must be in the project.')
        return super().validate(attrs)

    def create(self, validated_data):
        return super().create({**validated_data, 'creator': self.context['request'].user})


class TaskGetSerializer(serializers.ModelSerializer):
    assignee = account_serializers.UserSerializer(many=False, read_only=True)
    creator = account_serializers.UserSerializer(many=False, read_only=True)

    class Meta:
        model = project_models.Task
        fields = ('id', 'creator', 'title', 'description', 'status',
                  'project', 'assignee', 'created_at', 'updated_at')


class ProjectCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_models.Project
        fields = ('id', 'title', 'description', 'creator', 'assignees')
        extra_kwargs = {'assignees': {'required': False}}
        read_only_fields = ('creator',)

    def create(self, validated_data):
        return super().create({**validated_data, 'creator': self.context['request'].user})


class ProjectGetSerializer(serializers.ModelSerializer):
    assignees = account_serializers.UserSerializer(many=True, read_only=True)
    creator = account_serializers.UserSerializer(many=False, read_only=True)
    tasks = TaskGetSerializer(many=True, read_only=True)

    class Meta:
        model = project_models.Project
        fields = ('id', 'creator', 'title', 'description', 'tasks',
                  'assignees', 'created_at', 'updated_at')
