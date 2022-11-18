from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from roles.models import Role
from users.models import User


class TestUser(APITestCase):
    email = 'test@gmail.com'
    first_name = 'test',
    last_name = 'test',
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "employee"
        self.role = Role.objects.create(name=self.role_name)
        self.add_permission = Permission.objects.get(name='Can add user')
        self.view_permission = Permission.objects.get(name='Can view user')
        self.list_permission = Permission.objects.get(name='Can list user')
        self.change_permission = Permission.objects.get(name='Can change user')
        self.delete_permission = Permission.objects.get(name='Can delete user')
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            role=self.role)
        self.user1 = {"email": "test2@gmail.com", "password": "test2@123", "confirm_password": "test2@123",
                      "first_name": "test2", "last_name": "test2", "username": "test2", "role": self.role.id}
        self.user_create_url = reverse('register_employee')
        self.user_list_url = reverse('list_employee')
        self.user_retrieve_update_delete_url = reverse('retrieve_update_delete_employee', kwargs={'id': self.user.id})

    def test_add_user_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.user_create_url, self.user1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_add_user_same_username_denied(self):
        self.user.user_permissions.add(self.add_permission)
        data = {"email": "test2@gmail.com", "password": "test2@123", "confirm_password": "test2@123",
                "first_name": "test2", "last_name": "test2", "username": "test", "role": self.role.id}
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.user_create_url, data)
        self.assertEqual(r.status_code, 400)

    def test_add_user_with_permission(self):
        self.user.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.user_create_url, self.user1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['username'], "test2")

    def test_list_user_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.user_list_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_user_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.user_list_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['username'], "test")

    def test_get_user_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.user_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_get_user_with_permission(self):
        self.user.user_permissions.add(self.view_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.user_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['username'], "test")

    def test_update_user_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.user_retrieve_update_delete_url, self.user1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_update_user_with_permission(self):
        self.user.user_permissions.add(self.change_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.user_retrieve_update_delete_url, self.user1)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['username'], "test2")

    def test_delete_user_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.delete(self.user_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_delete_user_with_permission(self):
        self.user.user_permissions.add(self.delete_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.delete(self.user_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.data, {})


class TestLogin(APITestCase):
    email = 'test@gmail.com'
    first_name = 'test',
    last_name = 'test',
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "employee"
        self.role = Role.objects.create(name=self.role_name)
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            role=self.role)
        self.user1 = {"username": "test2", "password": "test2@123"}
        self.user_login_create_url = reverse('token_obtain_pair')

    def test_login_no_user(self):
        r = self.client.post(self.user_login_create_url, self.user1)
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.data["detail"], "No active account found with the given credentials")

    def test_login_success(self):
        data = {"username": "test", "password": "test@123"}
        r = self.client.post(self.user_login_create_url, data)
        self.assertEqual(r.status_code, 200)
