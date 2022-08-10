from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class TokenReceivingTest(APITestCase):
    def test_token_receiving(self):
        url = '/api/v1/registration/'
        data = {'username': 'gomer', 'password': '2345dfghj!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'gomer')

        url_2 = '/api-token-auth/'
        response_2 = self.client.post(url_2, data, format='json')
        token = response_2.data['token']
        self.assertEqual(response_2.status_code, status.HTTP_200_OK)
        self.assertEqual(Token.objects.get(user_id=3).key, token)

    def test_invalid_password(self):
        url = '/api/v1/registration/'
        data = {'username': 'gomer', 'password': '2345dfghj!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'gomer')

        url_2 = '/api-token-auth/'
        data = {'username': 'gomer', 'password': '2345dghj!'}
        response_2 = self.client.post(url_2, data, format='json')

        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.content, b'{"non_field_errors":["Unable to log in with provided credentials."]}')

    def test_invalid_username(self):
        url = '/api/v1/registration/'
        data = {'username': 'gomer', 'password': '2345dfghj!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'gomer')

        url_2 = '/api-token-auth/'
        data = {'username': 'gomr', 'password': '2345dfghj!'}
        response_2 = self.client.post(url_2, data, format='json')

        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.content, b'{"non_field_errors":["Unable to log in with provided credentials."]}')
