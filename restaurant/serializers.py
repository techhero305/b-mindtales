from rest_framework import serializers

from restaurant.models import Restaurant, FoodItem, Menu


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Serializer for restaurant
    """

    owner = serializers.SerializerMethodField('get_owner')

    def get_owner(self, restaurant_obj):
        return restaurant_obj.owner.username

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'owner']


class FoodItemSerializer(serializers.ModelSerializer):
    """
    Serializer for food item
    """

    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'price', 'food_type', 'restaurant']


class MenuSerializer(serializers.ModelSerializer):
    """
    Serializer for menu
    """

    class Meta:
        model = Menu
        fields = ['id', 'day', 'restaurant', 'food_item', 'date_time']
