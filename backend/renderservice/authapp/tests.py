from django.contrib.auth.models import User
from rest_framework import status

from rest_framework.test import APITestCase


class UserRegisterTests(APITestCase):
    def test_create_user(self):
        url = '/api/v1/registration/'
        data = {'username': 'gomer', 'password': '2345dfghj!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'gomer')

        data_2 = {'username': 'gomer_2', 'password': '2345dfghj!'}
        response_2 = self.client.post(url, data_2, format='json')

        self.assertEqual(response_2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.get(id=3).username, 'gomer_2')

        data_3 = {'username': 'gomer_3', 'password': '2345dfghj!'}
        response_3 = self.client.post(url, data_3, format='json')

        self.assertEqual(response_3.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(id=4).username, 'gomer_3')

        data_4 = {'username': 'gomer_4', 'password': '2345dfghj!'}
        response_4 = self.client.post(url, data_4, format='json')

        self.assertEqual(response_4.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)
        self.assertEqual(User.objects.get(id=5).username, 'gomer_4')

        data_5 = {'username': 'gomer_5', 'password': '2345dfghj!'}
        response_5 = self.client.post(url, data_5, format='json')

        self.assertEqual(response_5.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 5)
        self.assertEqual(User.objects.get(id=6).username, 'gomer_5')

    def test_error_400(self):
        url = '/api/v1/registration/'
        data = {'username': '', 'password': '2345dfghj!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data_2 = {'username': 'gomer', 'password': ''}
        response_2 = self.client.post(url, data_2, format='json')

        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_exists_user(self):
        url = '/api/v1/registration/'
        data = {'username': 'gomer', 'password': '2345dfghj!'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        url = '/api/v1/registration/'
        data_2 = {'username': 'gomer', 'password': '2345dfghj!'}
        response_2 = self.client.post(url, data_2, format='json')

        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_2.content,
            b'{"username":["A user with that username '
            b'already exists."]}'
        )


