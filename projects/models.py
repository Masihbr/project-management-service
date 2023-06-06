from typing import Iterable, Optional
from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="created_projects")
    assignees = models.ManyToManyField(
        "accounts.User", blank=True, related_name="assigned_projects")

    def has_assignee(self, user):
        return self.assignees.filter(id=user.id).exists()

    def __str__(self) -> str:
        return f"{self.creator}:{self.title}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="created_tasks")
    assignee = models.ForeignKey(
        "accounts.User", on_delete=models.CASCADE, related_name="assigned_tasks")
    project = models.ForeignKey(
        "projects.Project", on_delete=models.CASCADE, related_name="tasks")

    def __str__(self) -> str:
        return f"{self.project}${self.creator}:{self.title}"
