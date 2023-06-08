from projects import models as project_models
from accounts import models as account_models


class BaseQuerySetProvider:
    @classmethod
    def get_queryset(cls, user: account_models.User):
        raise NotImplementedError()

class ProjectQuerySetProvider(BaseQuerySetProvider):
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


class TaskQuerySetProvider(BaseQuerySetProvider):
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
