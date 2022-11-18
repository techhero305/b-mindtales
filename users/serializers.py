from rest_framework import serializers

from users.models import User


class EmployeeRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for register employee.
    """
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'role', 'email', 'username', 'password', 'confirm_password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError({"validation_error": "Password and Confirm Password doesn't match"})
        data.pop('confirm_password')
        return data

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee
    """

    class Meta:
        model = User
        fields = ['id', 'role', 'email', 'username', 'first_name', 'last_name']
