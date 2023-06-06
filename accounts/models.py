from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Role(models.TextChoices):
        DEVELOPER = 'developer', _('Developer')
        PROJECT_MANAGER = 'project_manager', _('Project Manager')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        null=True,
        default=None,
        verbose_name=_('Role'),
    )
    
    @property
    def is_developer(self):
        return self.role == self.Role.DEVELOPER.value
    
    @property
    def is_project_manager(self):
        return self.role == self.Role.PROJECT_MANAGER.value
