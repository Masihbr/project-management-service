from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from accounts import models as account_models
from projects import models as project_models

GROUPS_PERMISSIONS = {
    account_models.User.Role.DEVELOPER.value: {
        project_models.Project: ['view'],
    },
    account_models.User.Role.PRODUCT_MANAGER.value: {
        project_models.Project: ['view', 'add', 'change'],
    },
}

ALLOWED_GENERIC_PERMISSIONS = ['add', 'view', 'change']


def get_model_generic_permission(model_class, generic_permission):
    if generic_permission not in ALLOWED_GENERIC_PERMISSIONS:
        raise Exception(
            f"generic_permission [{generic_permission}] not in ({ALLOWED_GENERIC_PERMISSIONS})")
    content_type = ContentType.objects.get_for_model(model_class)
    codename = generic_permission + "_" + model_class._meta.model_name
    return Permission.objects.get(
        content_type=content_type,
        codename=codename)


def setup_groups():
    for group_name in GROUPS_PERMISSIONS:
        group, _ = Group.objects.get_or_create(name=group_name)
        for model_cls in GROUPS_PERMISSIONS[group_name]:
            for perm_name in GROUPS_PERMISSIONS[group_name][model_cls]:
                perm = get_model_generic_permission(
                    model_class=model_cls, generic_permission=perm_name)
                group.permissions.add(perm)
                print(f"Adding {perm.codename} to group {group}")
