from rest_framework import viewsets, permissions
from projects import queryset_providers as project_queryset_providers
from projects import serializer_providers as project_serializer_providers


class BaseModelViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated,
                          permissions.DjangoModelPermissions]
    queryset_provider_class = None
    serializer_provider_class = None

    def get_queryset(self):
        return self.queryset_provider_class.get_queryset(self.request.user)

    def get_serializer_class(self, *args, **kwargs):
        return self.serializer_provider_class.get_serializer_class(self.action)


class ProjectModelViewSet(BaseModelViewSet):
    queryset_provider_class = project_queryset_providers.ProjectQuerySetProvider
    serializer_provider_class = project_serializer_providers.ProjectSerializerProvider


class TaskModelViewSet(BaseModelViewSet):
    queryset_provider_class = project_queryset_providers.TaskQuerySetProvider
    serializer_provider_class = project_serializer_providers.TaskSerializerProvider
