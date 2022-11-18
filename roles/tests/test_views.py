from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from roles.models import Role
from users.models import User


class TestRole(APITestCase):
    email = 'test@gmail.com'
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "restaurant_owner"
        self.role = Role.objects.create(name=self.role_name)
        self.role1 = {"name": "Test1"}
        self.add_permission = Permission.objects.get(name='Can add role')
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username,
            role=self.role)
        self.role_create_url = reverse('List_Create_Role')

    def test_add_role_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.role_create_url, self.role1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_add_role_with_permission(self):
        self.user.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.role_create_url, self.role1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['name'], "Test1")
