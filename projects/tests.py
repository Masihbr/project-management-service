from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.authorizations import setup_groups

from accounts import models as account_models
from projects import models as project_models


class BaseProjectsAPITestCase(APITestCase):
    PROJECT_MANAGERS_COUNT = 2
    DEVELOPERS_COUNT = 4

    def setUp(self) -> None:
        setup_groups(quiet=True)
        self.client = self.client_class()
        self.signup_url = reverse('sign-up')
        self.project_managers = [
            self.create_user(
                username=f"pm{i}",
                password=f"pm{i}password",
                role=account_models.User.Role.PROJECT_MANAGER.value
            ) for i in range(0, self.PROJECT_MANAGERS_COUNT)
        ]
        self.developers = [
            self.create_user(
                username=f"dv{i}",
                password=f"dv{i}password",
                role=account_models.User.Role.DEVELOPER.value
            ) for i in range(0, self.DEVELOPERS_COUNT)
        ]

    def create_user(self, username: str, password: str, role: str) -> account_models.User:
        signup_url = reverse('sign-up')
        valid_payload = {
            'username': username,
            'password': password,
            'role': role
        }
        self.client.post(
            signup_url,
            data=valid_payload,
            format='json'
        )
        return account_models.User.objects.get(username=username)

    def create_project(self, user: account_models.User, payload: dict):
        create_project_url = reverse('projects-crud-list')
        self.client.force_login(user)
        return self.client.post(
            create_project_url,
            data=payload,
            format='json'
        )

    def update_project(self, user: account_models.User, project: project_models.Project, payload: dict):
        update_project_url = reverse('projects-crud-detail', args=[project.id])
        self.client.force_login(user)
        return self.client.patch(
            update_project_url,
            data=payload,
            format='json'
        )

    def get_projects(self, user: account_models.User):
        list_project_url = reverse('projects-crud-list')
        self.client.force_login(user)
        return self.client.get(
            list_project_url
        )


class ProjectAPITestCase(BaseProjectsAPITestCase):

    def test_project_manager_creates_projects(self):
        project_creation_payload = {
            'title': 'test title',
            'description': 'test desc',
        }
        response = self.create_project(
            self.project_managers[0], project_creation_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(project_models.Project.objects.count(), 1)
        does_project_exist: bool = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).exists()
        self.assertEqual(does_project_exist, True)

    def test_project_manager_assigns_developers_to_project(self):
        assignees = [self.developers[0].id, self.developers[1].id]
        project_creation_payload = {
            'title': 'test title',
            'description': 'test desc',
            'assignees': assignees
        }
        response = self.create_project(
            self.project_managers[0], project_creation_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(project_models.Project.objects.count(), 1)
        project = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).last()
        self.assertIsNotNone(project)
        self.assertEqual(project.assignees.count(), len(assignees))

        new_assignees = [*assignees,
                         self.developers[2].id, self.developers[3].id]
        project_update_payload = {
            'assignees': new_assignees
        }
        response = self.update_project(
            self.project_managers[0], project, project_update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).last()
        self.assertEqual(project.assignees.count(), len(new_assignees))

    def test_project_manager_removes_developers_from_project(self):
        assignees = [self.developers[0].id, self.developers[1].id]
        project_creation_payload = {
            'title': 'test title',
            'description': 'test desc',
            'assignees': assignees
        }
        response = self.create_project(
            self.project_managers[0], project_creation_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(project_models.Project.objects.count(), 1)
        project = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).last()
        self.assertIsNotNone(project)
        self.assertEqual(project.assignees.count(), len(assignees))

        assignees.remove(self.developers[0].id)
        project_update_payload = {
            'assignees': assignees
        }
        response = self.update_project(
            self.project_managers[0], project, project_update_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        project = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).last()
        self.assertEqual(project.assignees.count(), len(assignees))
        self.assertFalse(project.has_assignee(self.developers[0]))

    def test_developer_can_view_their_projects(self):
        assignees = [self.developers[0].id, self.developers[1].id]
        project_creation_payload = {
            'title': 'test title',
            'description': 'test desc',
            'assignees': assignees
        }
        response = self.create_project(
            self.project_managers[0], project_creation_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.get_projects(self.developers[0])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = response.json()
        self.assertEqual(response_json[0].get(
            'title'), project_creation_payload['title'])
        self.assertEqual(response_json[0].get(
            'description'), project_creation_payload['description'])

    def test_developer_can_not_create_projects(self):
        project_creation_payload = {
            'title': 'test title',
            'description': 'test desc',
        }
        response = self.create_project(
            self.developers[0], project_creation_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(project_models.Project.objects.count(), 0)
        does_project_exist: bool = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).exists()
        self.assertEqual(does_project_exist, False)

    def test_developer_can_not_update_project(self):
        assignees = [self.developers[0].id, self.developers[1].id]
        project_creation_payload = {
            'title': 'test title',
            'description': 'test desc',
            'assignees': assignees
        }
        response = self.create_project(
            self.project_managers[0], project_creation_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        project = project_models.Project.objects.filter(
            title=project_creation_payload['title'], description=project_creation_payload['description']).last()

        project_update_payload = {
            'title': 'test2'
        }
        response = self.update_project(
            self.developers[0], project, project_update_payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
