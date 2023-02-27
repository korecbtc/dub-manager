from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from users.models import User
from tasks.models import Task
from projects.models import Project, Client
from django.test import override_settings


class TasksProjectsClientsUsersTests(APITestCase):

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
        'comments': 'Hi!',
        'time_create': '2023-02-25T12:06:41.098204Z'
        }
    TASK_DATA_POST = {
        'what_needed': 'Go-Go',
        'type': 'send',
        'urgency': 'now',
        'project': 1,
        'description': 'test task',
        'status': 'in_progress',
        'comments': 'Hi!',
        'time_create': '2023-02-25T12:06:41.098204Z'
        }
    TASK_DATA_PATCH = {
        'what_needed': 'Go-Go!',
        'type': 'receive',
        'urgency': 'day',
        'project': 1,
        'description': 'test task patched',
        'status': 'finished',
        'comments': 'Hi!!!!'
        }
    TASK_MUST_BE_POST = {
        'id': 2,
        'what_needed': 'Go-Go',
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
        'comments': None,
        'time_create': '2023-02-25T12:06:41.098204Z'
        }
    TASK_MUST_BE_POST_BY_ADMIN = {
        'id': 2,
        'what_needed': 'Go-Go',
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
        'comments': 'Hi!',
        'time_create': '2023-02-25T12:06:41.098204Z'
        }
    TASK_MUST_BE_PATCH = {
        'id': 2,
        'what_needed': 'Go-Go!',
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
        'comments': None,
        'time_create': '2023-02-25T12:06:41.098204Z'
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
        'status': 'finished',
        'comments': 'Hi!!!!',
        'time_create': '2023-02-25T12:06:41.098204Z'
        }
    TASK_MUST_BE_PATCH_BY_ADMIN = {
        'id': 2,
        'what_needed': 'Go-Go!',
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
        'status': 'finished',
        'comments': 'Hi!!!!',
        'time_create': '2023-02-25T12:06:41.098204Z'
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
    PROJECT_MUST_BE_POST = {
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
    CLIENT_MUST_BE = {
        'id': 1,
        'name': 'First',
        'address': 'Moscow',
        'email': 'first@ya.ru',
        'description': 'test client'
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
    CLIENT_MUST_BE_POST = {
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
    USER_DATA = {
        'username': 'newuser',
        'password': 'pass!!!word',
        'email': 'newuser@yandex.ru',
        'first_name': 'Новый',
        'last_name': 'Юзер',
        'role': 'manager'
        }
    USER_MUST_BE_POST = {
        'first_name': 'Новый',
        'last_name': 'Юзер',
        'email': 'newuser@yandex.ru',
        'role': 'manager',
        'username': 'newuser'
        }
    USER_DATA_PATCH = {
        'first_name': 'Патч',
        'last_name': 'Юзер',
        'email': 'newuserpatched@yandex.ru',
        'role': 'executer',
        'username': 'newuser_patched'
        }
    USER_MUST_BE_PATCH = {
        'id': 1,
        'first_name': 'Патч',
        'last_name': 'Юзер',
        'email': 'newuserpatched@yandex.ru',
        'role': 'executer',
        'username': 'newuser_patched'
        }

    def setUp(self):
        manager = User.objects.create(
            username='manager',
            password='123pass123',
            email='manager@ya.ru',
            role='manager',
        )
        manager.save()
        another_manager = User.objects.create(
            username='another_manager',
            password='123pass123',
            email='another_manager@ya.ru',
            role='manager',
        )
        another_manager.save()
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
        self.token_another_manager = Token.objects.create(user=another_manager)
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
            comments='Hi!',
            time_create='2023-02-25T12:06:41.098204Z'
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
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.TASK_MUST_BE)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.TASK_MUST_BE)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.TASK_MUST_BE)

    def test_projects_get(self):
        '''Проверка GET запросов на эндпоинт /api/projects/'''
        url = '/api/projects/'
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.PROJECT_MUST_BE)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.PROJECT_MUST_BE)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.PROJECT_MUST_BE)

    def test_clients_get(self):
        '''Проверка GET запросов на эндпоинт /api/clients/'''
        url = '/api/clients/'
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.CLIENT_MUST_BE)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()['results']), 1)
        self.assertEqual(response.json()['results'][0], self.CLIENT_MUST_BE)

    def test_only_admin_get_user_list(self):
        '''Проверка что список пользователей доступен только админу'''
        url = '/api/users/'
        self.client.logout()
        response = self.login_with(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.login_with(url, self.token_manager.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.login_with(url, self.token_executer.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.login_with(url, self.token_admin.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 4)

    def test_guest_cant_create_patch_delete_user(self):
        '''Неавторизированный пользователь не может создать пользователя'''
        self.client.logout()
        response = self.client.post(
            '/api/users/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_manager_cant_create_patch_delete_user(self):
        '''Менеджер не может создавать, изменять, удалять пользователей'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/users/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            '/api/users/1/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            '/api/users/1/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/users/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_executer_cant_create_patch_delete_user(self):
        '''Исполнитель не может создавать, изменять, удалять пользователей'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_executer.key
            )
        response = self.client.post(
            '/api/users/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            '/api/users/1/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            '/api/users/1/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/users/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_patch_delete_user(self):
        '''Администратор может создавать, изменять, удалять пользователей'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/users/', self.USER_DATA, format='json'
            )
        self.assertEqual(response.data, self.USER_MUST_BE_POST)
        response = self.client.patch(
            '/api/users/1/', self.USER_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.USER_MUST_BE_PATCH)
        response = self.client.put(
            '/api/users/1/', self.USER_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.USER_MUST_BE_PATCH)
        response = self.client.delete('/api/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tasks_post_guest(self):
        '''Проверка недоступности для неавторизированного пользователя'''
        self.client.logout()
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tasks_post_patch_put_delete_manager(self):
        '''Менеджер может менять все поля своей задачи,'''
        '''кроме статуса и комментария'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_POST)
        response = self.client.patch(
            '/api/tasks/2/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH)
        response = self.client.put(
            '/api/tasks/2/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH)
        response = self.client.delete('/api/tasks/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_another_manager.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.patch(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            '/api/tasks/1/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/tasks/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tasks_post_patch_put_delete_executer(self):
        '''Исполнитель может изменить только 2 поля: статус и комментарии'''
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
        '''Админ может создавать, изменять, удалять задачи'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/tasks/', self.TASK_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_POST_BY_ADMIN)
        response = self.client.patch(
            '/api/tasks/2/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH_BY_ADMIN)
        response = self.client.put(
            '/api/tasks/2/', self.TASK_DATA_PATCH, format='json'
            )
        self.assertEqual(response.data, self.TASK_MUST_BE_PATCH_BY_ADMIN)
        response = self.client.delete('/api/tasks/2/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_projects_post_guest(self):
        '''Проверка недоступности проектов для'''
        '''неавторизированного пользователя'''
        self.client.logout()
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_projects_post_patch_put_delete_manager(self):
        '''Менеджер может создавать, изменять, удалять только свои проекты'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE_POST)
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
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_another_manager.key
            )
        response = self.client.patch(
            '/api/projects/1/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.put(
            '/api/projects/1/', self.PROJECT_DATA_PATCH, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete('/api/projects/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_projects_post_patch_put_delete_executer(self):
        '''Исполнитель не может создавать, изменять, удалять проекты'''
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
        '''Админ может создавать, изменять, удалять проекты'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/projects/', self.PROJECT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.PROJECT_MUST_BE_POST)
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
        '''Проверка недоступности clients для'''
        '''неавторизированного пользователя'''
        self.client.logout()
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_clients_post_patch_put_delete_manager(self):
        '''Менеджер может создавать, изменять, удалять клиентов'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_manager.key
            )
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE_POST)
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
        '''Исполнитель не может создавать, изменять, удалять клиентов'''
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
        '''Админ может создавать, изменять, удалять клиентов'''
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token_admin.key
            )
        response = self.client.post(
            '/api/clients/', self.CLIENT_DATA_POST, format='json'
            )
        self.assertEqual(response.data, self.CLIENT_MUST_BE_POST)
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
