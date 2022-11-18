from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from restaurant.models import Restaurant, FoodItem, Menu
from roles.models import Role
from users.models import User


class TestRestaurant(APITestCase):
    email = 'test@gmail.com'
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "restaurant_owner"
        self.role = Role.objects.create(name=self.role_name)
        self.add_permission = Permission.objects.get(name='Can add restaurant')
        self.view_permission = Permission.objects.get(name='Can view restaurant')
        self.list_permission = Permission.objects.get(name='Can list restaurant')
        self.change_permission = Permission.objects.get(name='Can change restaurant')
        self.delete_permission = Permission.objects.get(name='Can delete restaurant')
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username,
            role=self.role)
        self.restaurant = Restaurant.objects.create(name="TGT", owner=self.user)
        self.restaurant1 = {"name": "TGM", "owner": self.user}
        self.restaurant_updated_data = {"name": "TGT", "owner": self.user}
        self.restaurant_list_create_url = reverse('list_register_restaurant')
        self.restaurant_retrieve_update_delete_url = reverse('retrieve_update_delete_restaurant',
                                                             kwargs={'id': self.restaurant.id})

    def test_add_restaurant_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.restaurant_list_create_url, self.restaurant1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_add_restaurant_with_permission(self):
        self.user.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.restaurant_list_create_url, self.restaurant1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['name'], "TGM")

    def test_list_restaurant_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.restaurant_list_create_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_restaurant_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.restaurant_list_create_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['name'], "TGT")

    def test_get_restaurant_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.restaurant_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_get_restaurant_with_permission(self):
        self.user.user_permissions.add(self.view_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.restaurant_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "TGT")

    def test_update_restaurant_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.restaurant_retrieve_update_delete_url, self.restaurant_updated_data)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_update_restaurant_with_permission(self):
        self.user.user_permissions.add(self.change_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.restaurant_retrieve_update_delete_url, self.restaurant_updated_data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "TGT")

    def test_delete_restaurant_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.delete(self.restaurant_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_delete_restaurant_with_permission(self):
        self.user.user_permissions.add(self.delete_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.delete(self.restaurant_retrieve_update_delete_url)
        self.assertEqual(r.status_code, 204)
        self.assertEqual(r.data, {})


class TestFoodItem(APITestCase):
    email = 'test@gmail.com'
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "restaurant_owner"
        self.role = Role.objects.create(name=self.role_name)
        self.add_permission = Permission.objects.get(name='Can add food item')
        self.view_permission = Permission.objects.get(name='Can view food item')
        self.list_permission = Permission.objects.get(name='Can list food item')
        self.change_permission = Permission.objects.get(name='Can change food item')
        self.user = User.objects.create_user(
            email=self.email,
            password=self.password,
            username=self.username,
            role=self.role)
        self.restaurant = Restaurant.objects.create(name="TGT", owner=self.user)
        self.food_item = FoodItem.objects.create(name="Paneer", restaurant=self.restaurant, description="Nice dish",
                                                 price=400, food_type='entree')
        self.food_item1 = {"name": "Naan", "restaurant": self.restaurant.id, "description": "Type of Roti", "price": 50,
                           "food_type": 'entree'}
        self.food_item_updated_data = {"name": "Paneer Tikka", "restaurant": self.restaurant.id,
                                       "description": "Nice dish", "price": 400, "food_type": 'entree'}
        self.food_item_list_create_url = reverse('list_add_food_item')
        self.food_item_retrieve_update_url = reverse('retrieve_update_food_item', kwargs={'id': self.food_item.id})

    def test_add_food_item_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.food_item_list_create_url, self.food_item1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_add_food_item_with_permission(self):
        self.user.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.food_item_list_create_url, self.food_item1)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.data['name'], "Naan")

    def test_list_food_item_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.food_item_list_create_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_restaurant_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.food_item_list_create_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['name'], "Paneer")

    def test_get_food_item_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.food_item_retrieve_update_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_get_food_item_with_permission(self):
        self.user.user_permissions.add(self.view_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.food_item_retrieve_update_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "Paneer")

    def test_update_food_item_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.food_item_retrieve_update_url, self.food_item_updated_data)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_update_food_item_with_permission(self):
        self.user.user_permissions.add(self.change_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.food_item_retrieve_update_url, self.food_item_updated_data)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['name'], "Paneer Tikka")


class TestMenu(APITestCase):
    email = 'test@gmail.com'
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "restaurant_owner"
        self.role = Role.objects.create(name=self.role_name)
        self.add_permission = Permission.objects.get(name='Can add menu')
        self.view_permission = Permission.objects.get(name='Can view menu')
        self.list_permission = Permission.objects.get(name='Can list menu')
        self.change_permission = Permission.objects.get(name='Can change menu')
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
        self.menu1 = {"restaurant": self.restaurant.id, "day": "Thursday",
                      "food_item": [self.food_item.id, self.food_item2.id]}
        self.menu_updated_data = {"day": "Thursday", "restaurant": self.restaurant.id, "food_item": [self.food_item.id]}
        self.menu_list_create_url = reverse('list_add_menu')
        self.menu_retrieve_update_url = reverse('retrieve_update_menu', kwargs={'id': self.menu.id})

    def test_add_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.menu_list_create_url, self.menu1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_add_menu_other_user_permission_denied(self):
        self.user2.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user2)
        r = self.client.post(self.menu_list_create_url, self.menu1)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["error"], "Permission denied")

    def test_add_menu_already_exists_with_permission(self):
        self.user.user_permissions.add(self.add_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.post(self.menu_list_create_url, self.menu1)
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.data['message'], "Cannot upload more than one menu")

    def test_list_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.menu_list_create_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_menu_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.menu_list_create_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['restaurant'], self.restaurant.id)

    def test_get_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.menu_retrieve_update_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_get_menu_with_permission(self):
        self.user.user_permissions.add(self.view_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.menu_retrieve_update_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['restaurant'], self.restaurant.id)

    def test_update_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.menu_retrieve_update_url, self.menu_updated_data, format='json')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_update_menu_other_user_permission_denied(self):
        self.user2.user_permissions.add(self.change_permission)
        self.client.force_authenticate(user=self.user2)
        r = self.client.put(self.menu_retrieve_update_url, self.menu_updated_data, format='json')
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_update_menu_with_permission(self):
        self.user.user_permissions.add(self.change_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.put(self.menu_retrieve_update_url, self.menu_updated_data, format='json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data['food_item'], [self.food_item.id])


class TestTodayMenu(APITestCase):
    email = 'test@gmail.com'
    username = 'test'
    password = 'test@123'

    def setUp(self):
        self.role_name = "restaurant_owner"
        self.role = Role.objects.create(name=self.role_name)
        self.role2 = Role.objects.create(name="employee")
        self.add_permission = Permission.objects.get(name='Can add menu')
        self.view_permission = Permission.objects.get(name='Can view menu')
        self.list_permission = Permission.objects.get(name='Can list menu')
        self.change_permission = Permission.objects.get(name='Can change menu')
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
        self.menu_list_url = reverse('list_today_menu')

    def test_list_today_menu_permission_denied(self):
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.menu_list_url)
        self.assertEqual(r.status_code, 403)
        self.assertEqual(r.data["detail"], "You do not have permission to perform this action.")

    def test_list_today_menu_with_permission(self):
        self.user.user_permissions.add(self.list_permission)
        self.client.force_authenticate(user=self.user)
        r = self.client.get(self.menu_list_url)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.data[0]['restaurant'], self.restaurant.id)
