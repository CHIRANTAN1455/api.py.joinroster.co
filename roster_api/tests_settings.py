from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from roster_api.models import Setting

class SettingTests(APITestCase):
    def setUp(self):
        self.setting = Setting.objects.create(
            type='system',
            element='text',
            label='Site Name',
            key='site_name',
            value='Roster'
        )

    def test_list_settings(self):
        """Verify settings can be retrieved"""
        url = '/api/settings'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('settings', response.data)
        self.assertTrue(len(response.data['settings']) > 0)

    def test_filter_settings_by_type(self):
        """Verify settings can be filtered by type"""
        url = '/api/settings?type=system'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['settings'][0]['type'], 'system')

    def test_create_setting(self):
        """Verify a new setting can be added"""
        url = '/api/settings/add'
        data = {
            'type': 'api',
            'element': 'text',
            'label': 'API Key',
            'key': 'api_key',
            'value': 'secret123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Setting.objects.filter(key='api_key').count(), 1)

    def test_update_setting(self):
        """Verify a setting can be modified"""
        url = '/api/settings/update'
        data = {
            'site_name': 'New Roster Name'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.setting.refresh_from_db()
        self.assertEqual(self.setting.value, 'New Roster Name')

    def test_delete_setting(self):
        """Verify a setting can be deleted"""
        url = f'/api/settings/{self.setting.id}/delete'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Setting.objects.filter(id=self.setting.id).count(), 0)
