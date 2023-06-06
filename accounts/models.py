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
