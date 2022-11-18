from django.db import models

from restaurant.models import Menu
from users.models import User


class UserVote(models.Model):
    """
    Model for user votes
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("list_uservote", "Can list user vote")
        ]

    def __str__(self):
        return f"{self.user.username} - {self.menu.restaurant.name} - {self.menu.date_time}"
