from django.db import models

from users.models import User


class Restaurant(models.Model):
    """
    Model for restaurant
    """
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        db_table = 'Restaurant'
        permissions = [
            ("list_restaurant", "Can list restaurant")
        ]
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['owner_id'])
        ]

    def __str__(self):
        return f"{self.name} - {self.id}"


class FoodItem(models.Model):
    """
    Model for food item
    """

    food_type = (
        ("appetizer", "appetizer"),
        ("entree", "entree"),
        ("dessert", "dessert"),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    price = models.FloatField()
    food_type = models.CharField(max_length=12, choices=food_type)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ("list_fooditem", "Can list food item")
        ]

    def __str__(self):
        return f"{self.name} - {self.id}"


class Menu(models.Model):
    """
    Model for menu
    """

    day = (
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday"),
        ("Saturday", "Saturday"),
        ("Sunday", "Sunday")
    )

    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    food_item = models.ManyToManyField(FoodItem, through="MenuFoodItem")
    day = models.CharField(max_length=10, choices=day)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("list_menu", "Can list menu")
        ]

    def __str__(self):
        return f"{self.restaurant.name}"


class MenuFoodItem(models.Model):
    """
    Model for food item
    """
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    food_item = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
