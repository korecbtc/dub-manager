from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from django.test import TestCase, Client
from users.models import User


class AccountTests(APITestCase):
    def setUp(self):
        manager = User.objects.create(
            username='manager',
            password='123pass123',
            email='manager@ya.ru',
            role='manager',
        )
        manager.save()
        self.token_manager = Token.objects.create(user=manager)

    def test_me(self):
        url = '/api/tasks/'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_manager.key)
        response = self.client.get(url, format='json')
        print(response)