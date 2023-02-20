from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase, Client
from users.models import User
from tasks.models import Task
from projects.models import Project, Client


class AccountTests(APITestCase):
    def setUp(self):
        self.CLIENT_MUST_BE = {
            'id': 1,
            'name': 'First',
            'address': 'Moscow',
            'email': 'first@ya.ru',
            'description': 'test client'
            }
        self.PROJECT_MUST_BE = {
            'id': 1,
            'name': 'Best',
            'client': 'First',
            'date': '2023-02-18',
            'status': 'in_progress',
            'description': 'test project',
            'manager': 'manager'
            }
        self.TASK_MUST_BE = {
            'id': 1,
            'what_needed': 'Go',
            'type': 'send',
            'urgency': 'now',
            'project': {
                'id': 1,
                'name': 'Best',
                'client': 'First',
                'date': '2023-02-18',
                'status': 'in_progress',
                'description': 'test project',
                'manager': 'manager'
                },
            'description': 'test task',
            'status': 'in_progress',
            'comments': 'Hi!'
            }
        manager = User.objects.create(
            username='manager',
            password='123pass123',
            email='manager@ya.ru',
            role='manager',
        )
        manager.save()
        executer = User.objects.create(
            username='executer',
            password='123pass123',
            email='executer@ya.ru',
            role='executer',
        )
        admin = User.objects.create(
            username='admin',
            password='123pass123',
            email='admin@ya.ru',
            role='admin',
        )
        self.token_manager = Token.objects.create(user=manager)
        self.token_executer = Token.objects.create(user=executer)
        self.token_admin = Token.objects.create(user=admin)
        self.clients = Client.objects.create(
            name='First',
            address='Moscow',
            email='first@ya.ru',
            description='test client'
        )
        self.project = Project.objects.create(
            name='Best',
            client=self.clients,
            date='2023-02-18',
            status='in_progress',
            description='test project',
            manager=manager
        )
        self.task = Task.objects.create(
            what_needed='Go',
            type='send',
            urgency='now',
            project=self.project,
            description='test task',
            status='in_progress',
            comments='Hi!'
        )
        self.TASK_MUST_BE = {
            'id': 1,
            'what_needed': 'Go',
            'type': 'send',
            'urgency': 'now',
            'project': {
                'id': 1,
                'name': 'Best',
                'client': 'First',
                'date': '2023-02-18',
                'status': 'in_progress',
                'description': 'test project',
                'manager': 'manager'
                },
            'description': 'test task',
            'status': 'in_progress',
            'comments': 'Hi!'
            }

    def login_with(self, url, token=None):
        if token is None:
            self.client.logout()
            return self.client.get(url, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token
            )
        return self.client.get(url, format='json')

    def test_tasks_get(self):
        url = '/api/tasks/'
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.TASK_MUST_BE)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.TASK_MUST_BE)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.TASK_MUST_BE)

    def test_projects_get(self):
        url = '/api/projects/'
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.PROJECT_MUST_BE)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.PROJECT_MUST_BE)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.PROJECT_MUST_BE)

    def test_clients_get(self):
        url = '/api/clients/'
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.CLIENT_MUST_BE)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0], self.CLIENT_MUST_BE)
