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
        elif self.request.user.role == account_models.User.Role.PRODUCT_MANAGER.value:
            return project_models.Project.objects.filter(creator=user)
        else:
            return project_models.Project.objects.none()
