from rest_framework import viewsets, permissions, generics
from projects import serializers as project_serializers
from projects import models as project_models
from accounts import models as account_models


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]
    queryset_provider_class = None
    serializer_provider_class = None

    def get_queryset(self):
        return self.queryset_provider_class.get_queryset(self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_provider_class.get_serializer_class(self.action)


class ProjectQuerySetProvider:
    @classmethod
    def get_queryset(cls, user: account_models.User):
        if user.is_superuser:
            return project_models.Project.objects.all()
        elif user.is_developer:
            return project_models.Project.objects.filter(assignees=user)
        elif user.is_project_manager:
            return project_models.Project.objects.filter(creator=user)
        else:
            return project_models.Project.objects.none()


class TaskQuerySetProvider:
    @classmethod
    def get_queryset(cls, user: account_models.User):
        if user.is_superuser:
            return project_models.Task.objects.all()
        elif user.is_developer:
            return project_models.Task.objects.filter(assignee=user)
        elif user.is_project_manager:
            projects = project_models.Project.objects.filter(creator=user)
            return project_models.Task.objects.filter(project__in=projects)
        else:
            return project_models.Task.objects.none()


class ProjectSerializerProvider:
    @classmethod
    def get_serializer_class(cls, action: str):
        if action in ('list', 'retrieve'):
            return project_serializers.ProjectListRetrieveSerializer
        else:  # create, update
            return project_serializers.ProjectCreateUpdateSerializer


class TaskSerializerProvider:
    @classmethod
    def get_serializer_class(cls, action: str):
        if action in ('list', 'retrieve'):
            return project_serializers.TaskListRetrieveSerializer
        elif action in ('update', 'partial_update'):
            return project_serializers.TaskUpdateSerializer
        else:  # create
            return project_serializers.TaskCreateSerializer


class ProjectModelViewSet(BaseModelViewSet):
    queryset_provider_class = ProjectQuerySetProvider
    serializer_provider_class = ProjectSerializerProvider


class TaskModelViewSet(BaseModelViewSet):
    queryset_provider_class = TaskQuerySetProvider
    serializer_provider_class = TaskSerializerProvider
