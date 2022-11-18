from django.contrib.auth.models import Group
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver

from roles.models import Role


@receiver(pre_save, sender=Role)
def update_group(sender, instance, **kwargs):
    if instance.id:
        name = Role.objects.get(id=instance.id).name
        group = Group.objects.get(name=name)
        group.name = instance.name
        group.save()
    else:
        Group.objects.get_or_create(name=instance.name)


@receiver(post_delete, sender=Role)
def delete_group(sender, instance, **kwargs):
    _, _ = sender, kwargs
    Group.objects.filter(name=instance.name).delete()
