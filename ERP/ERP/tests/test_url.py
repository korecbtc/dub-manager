from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User
from tasks.models import Task
from projects.models import Project, Client


class GetTests(APITestCase):

    CLIENT_MUST_BE = {
        'id': 1,
        'name': 'First',
        'address': 'Moscow',
        'email': 'first@ya.ru',
        'description': 'test client'
        }
    PROJECT_MUST_BE = {
        'id': 1,
        'name': 'Best',
        'client': 'First',
        'date': '2023-02-18',
        'status': 'in_progress',
        'description': 'test project',
        'manager': 'manager'
        }
    TASK_MUST_BE = {
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

    def setUp(self):
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
        executer.save()
        admin = User.objects.create(
            username='admin',
            password='123pass123',
            email='admin@ya.ru',
            role='admin',
        )
        admin.save()
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

    def login_with(self, url, token=None):
        '''Вспомогательная функция для авторизации'''
        if token is None:
            self.client.logout()
            return self.client.get(url, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + token
            )
        return self.client.get(url, format='json')

    def test_tasks_get(self):
        '''Проверка GET запросов на эндпоинт /api/tasks/'''
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
        '''Проверка GET запросов на эндпоинт /api/projects/'''
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
        '''Проверка GET запросов на эндпоинт /api/clients/'''
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

    def test_only_admin_get_user_list(self):
        '''Проверка что список пользователей доступен только админу'''
        url = '/api/users/'
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 3)


class PostPatchPutDeleteTests(APITestCase):

    TASK_DATA_POST = {
        'what_needed': 'Go',
        'type': 'send',
        'urgency': 'now',
        'project': 1,
        'description': 'test task',
        'status': 'in_progress',
        'comments': 'Hi!'
        }
    TASK_DATA_PATCH = {
        'what_needed': 'Go!',
        'type': 'receive',
        'urgency': 'day',
        'project': 1,
        'description': 'test task patched',
        'status': 'in_progress',
        'comments': 'Hi!'
        }
    PROJECT_DATA_POST = {
        'name': 'Best',
        'client': 1,
        'date': '2023-02-18',
        'status': 'in_progress',
        'description': 'test project',
        'manager': 1
        }
    PROJECT_DATA_PATCH = {
        'name': 'Terminator',
        'client': 1,
        'date': '2023-02-19',
        'status': 'finished',
        'description': 'test project pathced',
        'manager': 1
        }
    CLIENT_DATA_POST = {
        'name': 'First',
        'address': 'Moscow',
        'email': 'first1@ya.ru',
        'description': 'test client'
        }
    CLIENT_DATA_PATCH = {
        'name': 'Second',
        'address': 'MoscowCity',
        'email': 'first2@ya.ru',
        'description': 'test client patched'
        }
    CLIENT_MUST_BE = {
        'id': 2,
        'name': 'First',
        'address': 'Moscow',
        'email': 'first1@ya.ru',
        'description': 'test client'
        }
    CLIENT_MUST_BE_PATCHED = {
        'id': 2,
        'name': 'Second',
        'address': 'MoscowCity',
        'email': 'first2@ya.ru',
        'description': 'test client patched'
        }
    PROJECT_MUST_BE = {
        'id': 2,
        'name': 'Best',
        'client': 'First',
        'date': '2023-02-18',
        'status': 'in_progress',
        'description': 'test project',
        'manager': 'manager'
        }
    PROJECT_MUST_BE_PATCHED = {
        'id': 2,
        'name': 'Terminator',
        'client': 'First',
        'date': '2023-02-19',
        'status': 'finished',
        'description': 'test project pathced',
        'manager': 'manager'
    }
    TASK_MUST_BE_POST = {
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
        'status': 'not_viewed',
        'comments': None
        }
    TASK_MUST_BE_POST_BY_ADMIN = {
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
    TASK_MUST_BE_PATCH = {
        'id': 1,
        'what_needed': 'Go!',
        'type': 'receive',
        'urgency': 'day',
        'project': {
            'id': 1,
            'name': 'Best',
            'client': 'First',
            'date': '2023-02-18',
            'status': 'in_progress',
            'description': 'test project',
            'manager': 'manager'
            },
        'description': 'test task patched',
        'status': 'not_viewed',
        'comments': None
        }
    TASK_MUST_BE_PATCH_BY_EXECUTER = {
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
    TASK_MUST_BE_PATCH_BY_ADMIN = {
        'id': 1,
        'what_needed': 'Go!',
        'type': 'receive',
        'urgency': 'day',
        'project': {
            'id': 1,
            'name': 'Best',
            'client': 'First',
            'date': '2023-02-18',
            'status': 'in_progress',
            'description': 'test project',
            'manager': 'manager'
            },
        'description': 'test task patched',
        'status': 'in_progress',
        'comments': 'Hi!'
        }

    def setUp(self):
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
        executer.save()
        admin = User.objects.create(
            username='admin',
            password='123pass123',
            email='admin@ya.ru',
            role='admin',
        )
        admin.save()
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

    def test_tasks_post_guest(self):
        self.client.logout()
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tasks_post_patch_put_delete_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_POST)
        response = self.client.patch(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH)
        response = self.client.put(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH)
        response = self.client.delete('/api/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tasks_post_patch_put_delete_executer(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_executer.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH_BY_EXECUTER)
        response = self.client.put(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tasks_post_patch_put_delete_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_POST_BY_ADMIN)
        response = self.client.patch(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH_BY_ADMIN)
        response = self.client.put(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH_BY_ADMIN)
        response = self.client.delete('/api/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_projects_post_guest(self):
        self.client.logout()
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_projects_post_patch_put_delete_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE)
        response = self.client.patch(
            '/api/projects/2/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE_PATCHED)
        response = self.client.put(
            '/api/projects/2/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE_PATCHED)
        response = self.client.delete('/api/projects/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_projects_post_patch_put_delete_executer(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_executer.key
            )
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            '/api/projects/2/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            '/api/projects/2/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/projects/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_projects_post_patch_put_delete_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE)
        response = self.client.patch(
            '/api/projects/2/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE_PATCHED)
        response = self.client.put(
            '/api/projects/2/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE_PATCHED)
        response = self.client.delete('/api/projects/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_clients_post_guest(self):
        self.client.logout()
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_clients_post_patch_put_delete_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE)
        response = self.client.patch(
            '/api/clients/2/', self.CLIENT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE_PATCHED)
        response = self.client.put(
            '/api/clients/2/', self.CLIENT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE_PATCHED)
        response = self.client.delete('/api/clients/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_clients_post_patch_put_delete_executer(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_executer.key
            )
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            '/api/clients/2/', self.CLIENT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            '/api/clients/2/', self.CLIENT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/clients/2/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_clients_post_patch_put_delete_admin(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE)
        response = self.client.patch(
            '/api/clients/2/', self.CLIENT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE_PATCHED)
        response = self.client.put(
            '/api/clients/2/', self.CLIENT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE_PATCHED)
        response = self.client.delete('/api/clients/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
