from rest_framework import serializers

from roles.models import Role


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer to View List of roles, add role, update role, delete role, and retrieve role
    """

    class Meta:
        model = Role
        fields = '__all__'
