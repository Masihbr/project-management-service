from rest_framework import viewsets, permissions
from projects import serializers as project_serializers
from projects import models as project_models
from accounts import models as account_models


class ProjectModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('list', 'retrieve'):
            return project_serializers.ProjectListRetrieveSerializer
        return project_serializers.ProjectCreateUpdateSerializer

    def get_queryset(self):
        user: account_models.User = self.request.user
        if user.is_superuser:
            return project_models.Project.objects.all()
        elif user.is_developer:
            return project_models.Project.objects.filter(assignees=user)
        elif user.is_project_manager:
            return project_models.Project.objects.filter(creator=user)
        else:
            return project_models.Project.objects.none()


class TaskModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]

    def get_serializer_class(self, *args, **kwargs):
        if self.action in ('list', 'retrieve'):
            return project_serializers.TaskListRetrieveSerializer
        return project_serializers.TaskCreateUpdateSerializer

    def get_queryset(self):
        user: account_models.User = self.request.user
        if user.is_superuser:
            return project_models.Task.objects.all()
        elif user.is_developer:
            return project_models.Task.objects.filter(assignee=user)
        elif user.is_project_manager:
            projects = project_models.Project.objects.filter(creator=user)
            return project_models.Task.objects.filter(project__in=projects)
        else:
            return project_models.Task.objects.none()
