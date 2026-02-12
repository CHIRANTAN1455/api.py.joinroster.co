from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class HealthCheckTest(APITestCase):
    def test_health_check(self):
        url = '/api/test' # Based on urlpatterns in urls.py
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'API routes working fine!')
