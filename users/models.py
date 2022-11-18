from django.contrib.auth.models import AbstractUser
from django.db import models

from roles.models import Role


class User(AbstractUser):
    """
    Model for user details
    """
    role = models.ForeignKey(Role, on_delete=models.PROTECT)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    class Meta:
        db_table = 'AuthUsers'
        permissions = [
            ("list_user", "Can list user")
        ]
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role_id'])
        ]

    def __str__(self):
        return f"{self.username} - {self.id}"
