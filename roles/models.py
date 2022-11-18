from django.db import models


class Role(models.Model):
    """
    Model for roles
    """
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'User Roles'
        indexes = [
            models.Index(fields=['name']),
        ]
        permissions = [
            ("list_role", "Can list role"),
        ]

    def __str__(self):
        return f"{self.name}"
