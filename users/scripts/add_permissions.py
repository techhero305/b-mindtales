from django.contrib.auth.models import Group, Permission
from django.db import IntegrityError

from roles.models import Role
from users.models import User

ROLES = ["admin", "restaurant_owner", "employee"]
restaurant_owner_permissions = ['view_restaurant', 'list_restaurant', 'add_restaurant', 'change_restaurant',
                                'delete_restaurant',
                                'view_fooditem', 'add_fooditem', 'change_fooditem',
                                'delete_fooditem', 'list_fooditem',
                                'list_menu', 'view_menu', 'add_menu', 'change_menu']
employee_permissions = ['view_fooditem', 'list_fooditem', 'list_menu',
                        'view_menu', 'add_uservote', 'list_uservote']


def create_roles():
    for ROLE in ROLES:
        try:
            Role.objects.create(name=ROLE)
        except IntegrityError:
            print(f'{ROLE} already created')


def create_admin_permissions():
    admin_group = Group.objects.get(name="admin")
    admin_permissions = Permission.objects.all()
    for permission in admin_permissions:
        admin_group.permissions.add(permission)


def create_employee_permissions():
    employee_group = Group.objects.get(name="employee")
    permissions = Permission.objects.filter(codename__in=employee_permissions)
    for permission in permissions:
        employee_group.permissions.add(permission)


def create_restaurant_owner_permissions():
    restaurant_owner_group = Group.objects.get(name="restaurant_owner")
    permissions = Permission.objects.filter(codename__in=restaurant_owner_permissions)
    for permission in permissions:
        restaurant_owner_group.permissions.add(permission)


def create_super_user():
    admin_role = Role.objects.get(name="admin")
    try:
        User.objects.create_superuser(username="admin", email="admin@gmail.com", role=admin_role,
                                      password="admin", is_superuser=True, is_staff=True)
    except IntegrityError:
        print('Super User already exists')


def run():
    try:
        # Create roles
        create_roles()

        # Create admin permissions
        create_admin_permissions()

        # Create employee permissions
        create_employee_permissions()

        # Create restaurant owner permissions
        create_restaurant_owner_permissions()

        # Create Super User
        create_super_user()
    except AttributeError as e:
        print(f"Error: {e}")
