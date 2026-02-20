from rest_framework import status
from rest_framework.test import APITestCase
from roster_api.models import Users

class AdminTests(APITestCase):
    def setUp(self):
        self.editor = Users.objects.create(
            uuid='editor-uuid-123',
            name='Editor User',
            email='editor@example.com',
            account_type='editor',
            active=1,
            yt_verified=0
        )
        self.creator = Users.objects.create(
            uuid='creator-uuid-123',
            name='Creator User',
            email='creator@example.com',
            account_type='user',
            active=1,
            yt_verified=0
        )

    def test_list_editors(self):
        url = '/api/admin/editors'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('editors', response.data)
        self.assertEqual(len(response.data['editors']), 1)
        self.assertEqual(response.data['editors'][0]['uuid'], 'editor-uuid-123')

    def test_get_editor(self):
        url = f'/api/admin/editors/{self.editor.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['editor']['uuid'], 'editor-uuid-123')

    def test_list_creators(self):
        url = '/api/admin/creators'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('creators', response.data)
        self.assertEqual(len(response.data['creators']), 1)
        self.assertEqual(response.data['creators'][0]['uuid'], 'creator-uuid-123')

    def test_delete_account(self):
        url = '/api/admin/delete-account/creator@example.com'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.creator.refresh_from_db()
        self.assertEqual(self.creator.active, 0)
        self.assertIsNotNone(self.creator.deleted_at)
