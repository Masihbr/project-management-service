from django.urls import path
from django.urls.conf import include
from projects import views
from rest_framework import routers

projects_router = routers.SimpleRouter()
projects_router.register(
    "",
    views.ProjectModelViewSet,
    basename="projects-crud",
)

tasks_router = routers.SimpleRouter()
tasks_router.register(
    "",
    views.TaskModelViewSet,
    basename="tasks-crud",
)

urlpatterns = [
    path("crud/", include(projects_router.urls)),
    path("tasks/crud/", include(tasks_router.urls)),
]
