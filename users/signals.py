from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User


@receiver(post_save, sender=User)
def add_user_in_group(sender, instance, created, **kwargs):
    if not created:
        instance.groups.clear()
    group = Group.objects.get(name=instance.role.name)
    instance.groups.add(group)
