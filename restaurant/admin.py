from django.contrib import admin

from restaurant.models import Restaurant, FoodItem, Menu, MenuFoodItem

admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Menu)
admin.site.register(MenuFoodItem)
