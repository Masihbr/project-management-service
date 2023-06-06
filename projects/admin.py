from django.contrib import admin
from projects import models as project_models


@admin.register(project_models.Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "creator", "created_at", "updated_at", ]
    search_fields = ["creator"]


@admin.register(project_models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "creator", "assignee", "status", "created_at", "updated_at"]
    search_fields = ["creator", "assignee"]
