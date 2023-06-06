from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from accounts import serializers as account_serializers
from projects import serializers as project_serializers
from projects import models as project_models
from accounts import models as account_models

User = get_user_model()


class ProjectModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('list', 'retrieve'):
            return project_serializers.ProjectGetSerializer
        return project_serializers.ProjectCreateUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return project_models.Project.objects.all()
        if self.request.user.role == account_models.User.Role.DEVELOPER.value:
            return project_models.Project.objects.filter(assignees=user)
        elif self.request.user.role == account_models.User.Role.PROJECT_MANAGER.value:
            return project_models.Project.objects.filter(creator=user)
        else:
            return project_models.Project.objects.none()


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('list', 'retrieve'):
            return project_serializers.TaskGetSerializer
        return project_serializers.TaskCreateUpdateSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return project_models.Task.objects.all()
        if self.request.user.role == account_models.User.Role.DEVELOPER.value:
            projects = project_models.Project.objects.filter(assignees=user)
            return project_models.Task.objects.filter(project__in=projects)
        elif self.request.user.role == account_models.User.Role.PROJECT_MANAGER.value:
            projects = project_models.Project.objects.filter(creator=user)
            return project_models.Task.objects.filter(project__in=projects)
        else:
            return project_models.Task.objects.none()
