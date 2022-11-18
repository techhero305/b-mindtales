from django.urls import path

from restaurant.views import RestaurantListCreateView, RestaurantRetrieveUpdateDeleteView, FoodItemListCreateView, \
    FoodItemRetrieveUpdateView, MenuListCreateView, MenuRetrieveUpdateView, MenuListView

urlpatterns = [
    path('', RestaurantListCreateView.as_view(), name="list_register_restaurant"),
    path('<int:id>/', RestaurantRetrieveUpdateDeleteView.as_view(),
         name="retrieve_update_delete_restaurant"),
    path('food-item/', FoodItemListCreateView.as_view(), name="list_add_food_item"),
    path('food-item/<int:id>/', FoodItemRetrieveUpdateView.as_view(),
         name="retrieve_update_food_item"),
    path('menu/', MenuListCreateView.as_view(), name="list_add_menu"),
    path('menu/<int:id>/', MenuRetrieveUpdateView.as_view(),
         name="retrieve_update_menu"),
    path('menu/current-day/', MenuListView.as_view(),
         name="list_today_menu"),
]
