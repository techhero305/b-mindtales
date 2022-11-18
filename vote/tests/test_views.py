from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from restaurant.models import Restaurant, FoodItem, Menu
from roles.models import Role
from users.models import User
from vote.models import UserVote


class TestVote(APITestCase):
    email = 'test@gmail.com'
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "employee"
        self.role = Role.objects.create(name=self.role_name)
        self.add_permission = Permission.objects.get(name='Can add user vote')
        self.list_permission = Permission.objects.get(name='Can list user vote')
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username,
            role=self.role)
        self.user2 = User.objects.create_user(
            email="test2@gmail.com",
            password="test@123",
            username="test2",
            role=self.role)
        self.restaurant = Restaurant.objects.create(name="TGT", owner=self.user)
        self.food_item = FoodItem.objects.create(name="Paneer", restaurant=self.restaurant, description="Nice dish",
                                                 price=400, food_type='entree')
        self.food_item2 = FoodItem.objects.create(name="Naan", restaurant=self.restaurant, description="Type of Roti",
                                                  price=400, food_type='entree')
        self.menu = Menu.objects.create(restaurant=self.restaurant, day="Thursday")
        self.menu.food_item.set([self.food_item.id, self.food_item2.id])
        self.vote = UserVote.objects.create(user=self.user, menu=self.menu)
        self.vote2 = {"menu": self.menu.id}
        self.vote_create_url = reverse('Add_Vote')
        self.vote_list_url = reverse('List_Vote')
        self.vote_result_url = reverse('List_Result_Vote')

    def test_add_vote_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.vote_create_url, self.vote2)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_add_another_vote_permission_denied(self):
        self.user.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.vote_create_url, self.vote2)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.data["message"], "Already voted")

    def test_add_vote_with_permission(self):
        self.user2.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user2)
        r = self.client.post(self.vote_create_url, self.vote2)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['menu'], self.menu.id)

    def test_list_today_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.vote_list_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_vote_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.vote_list_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['menu'], self.menu.id)

    def test_list_result_today_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.vote_result_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_result_today_menu_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.vote_result_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['votes'], 1)
        self.assertEqual(r.data['restaurant'], "TGT")
