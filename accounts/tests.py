from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.authorizations import setup_groups

from accounts import models as account_models


class DeveloperSignUpAPITestCase(APITestCase):
    def setUp(self):
        setup_groups()
        self.client = self.client_class()
        self.signup_url = reverse('sign-up')
        self.username = 'user'
        self.password = 'password123'
        self.role = account_models.User.Role.DEVELOPER.value

    def test_create_valid_user(self):
        valid_payload = {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
        response = self.client.post(
            self.signup_url,
            data=valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(account_models.User.objects.count(), 1)
        self.assertEqual(account_models.User.objects.get().username, 'user')

    def test_create_invalid_user_missing_username(self):
        invalid_payload_missing_username = {
            'username': '',
            'password': self.password,
            'role': self.role,
        }
        response = self.client.post(
            self.signup_url,
            data=invalid_payload_missing_username,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(account_models.User.objects.count(), 0)

    def test_create_invalid_user_missing_password(self):
        invalid_payload_missing_password = {
            'username': self.username,
            'password': '',
            'role': self.role
        }
        response = self.client.post(
            self.signup_url,
            data=invalid_payload_missing_password,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(account_models.User.objects.count(), 0)

    def test_create_invalid_user_missing_role(self):
        invalid_payload_missing_password = {
            'username': self.username,
            'password': self.password,
            'role': ''
        }
        response = self.client.post(
            self.signup_url,
            data=invalid_payload_missing_password,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(account_models.User.objects.count(), 0)


class ProjectManagerSignUpAPITestCase(DeveloperSignUpAPITestCase):
    def setUp(self):
        super().setUp()
        self.role = account_models.User.Role.PROJECT_MANAGER.value


class DeveloperSignInAPITestCase(APITestCase):
    def setUp(self):
        setup_groups()
        self.client = self.client_class()
        self.login_url = reverse('login')
        self.username = 'user'
        self.password = 'password123'
        self.role = account_models.User.Role.DEVELOPER.value
        self.create_user()
        self.user = account_models.User.objects.get(username=self.username)
        
    def create_user(self):
        signup_url = reverse('sign-up')
        valid_payload = {
            'username': self.username,
            'password': self.password,
            'role': self.role
        }
        self.client.post(
            signup_url,
            data=valid_payload,
            format='json'
        )
    
    def test_login_valid_payload(self):
        valid_payload = {
            'username': self.username,
            'password': self.password,
        }
        response = self.client.post(
            self.login_url,
            data=valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_invalid_payload_wrong_password(self):
        invalid_payload = {
            'username': self.username,
            'password': 'wrong_password',
        }
        response = self.client.post(
            self.login_url,
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_invalid_payload_wrong_username(self):
        invalid_payload = {
            'username': 'wrong_username',
            'password': self.password,
        }
        response = self.client.post(
            self.login_url,
            data=invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProjectManagerSignInAPITestCase(DeveloperSignInAPITestCase):
    def setUp(self):
        setup_groups()
        self.client = self.client_class()
        self.login_url = reverse('login')
        self.username = 'user'
        self.password = 'password123'
        self.role = account_models.User.Role.PROJECT_MANAGER.value
        self.create_user()
        self.user = account_models.User.objects.get(username=self.username)