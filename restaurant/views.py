from datetime import date

from django.db.models import ProtectedError, Q
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from internal_menu_selection.common_permissions import IsAuthorizedForListModel, IsAuthorizedForModel
from internal_menu_selection.pagination import CustomPagination
from restaurant.models import Restaurant, FoodItem, Menu, MenuFoodItem
from restaurant.permissions import IsOwner, IsRestaurantOwner
from restaurant.serializers import RestaurantSerializer, FoodItemSerializer, MenuSerializer


class RestaurantListCreateView(generics.ListCreateAPIView):
    """
    View for creating restaurant and view list of all restaurants
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all().order_by('-id')
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name', '-id', '-name']
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsAuthorizedForListModel]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RestaurantRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, update and delete restaurant
    """
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAuthorizedForModel, IsOwner]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


class FoodItemListCreateView(generics.ListCreateAPIView):
    """
    View for creating food items and view list of all food items
    """
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all().order_by('-id')
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name', '-id', '-name']
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsAuthorizedForListModel]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant_id = request.data.get('restaurant')
        rest_obj = Restaurant.objects.get(id=restaurant_id)
        if request.user != rest_obj.owner:
            return Response({'error': "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FoodItemRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving, update and delete restaurant
    """
    serializer_class = FoodItemSerializer
    queryset = FoodItem.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAuthorizedForModel, IsRestaurantOwner]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuListCreateView(generics.ListCreateAPIView):
    """
    View for creating menu and view list of all menu
    """
    serializer_class = MenuSerializer
    queryset = Menu.objects.all().order_by('-id')
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['day']
    ordering_fields = ['id', 'name', '-id', '-name']
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsAuthorizedForListModel]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant_id = request.data.get('restaurant')
        rest_obj = Restaurant.objects.get(id=restaurant_id)
        if request.user != rest_obj.owner:
            return Response({'error': "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
        today = date.today()
        try:
            Menu.objects.get(restaurant=rest_obj, date_time__day=today.day)
            return Response({"message": "Cannot upload more than one menu"}, status=status.HTTP_400_BAD_REQUEST)
        except Menu.DoesNotExist:
            pass
        menu_data = serializer.save()

        for food_item_id in request.data.get("food_item", []):
            try:
                food_item_obj = FoodItem.objects.get(Q(id=food_item_id) & Q(restaurant=rest_obj))
                menu_data.food_item.add(food_item_obj)
            except FoodItem.DoesNotExist:
                pass

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MenuRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving, update menu
    """
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    lookup_field = 'id'
    permission_classes = [IsAuthenticated, IsAuthorizedForModel, IsRestaurantOwner]

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        restaurant_id = request.data.get('restaurant')
        rest_obj = Restaurant.objects.get(id=restaurant_id)
        if request.user != rest_obj.owner:
            return Response({'error': "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        if "food_item" in request.data:
            MenuFoodItem.objects.filter(menu=instance).delete()
        for food_item_id in request.data.get("food_item", []):
            try:
                food_item_obj = FoodItem.objects.get(Q(id=food_item_id) & Q(restaurant=rest_obj))
                instance.food_item.add(food_item_obj)
            except FoodItem.DoesNotExist:
                pass
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class MenuListView(generics.ListAPIView):
    """
    View for list of all menu
    """
    serializer_class = MenuSerializer
    queryset = Menu.objects.all().order_by('-id')
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['day']
    ordering_fields = ['id', 'name', '-id', '-name']
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsAuthorizedForListModel]

    def get(self, request, *args, **kwargs):
        today = date.today()
        today_menu = Menu.objects.filter(date_time__day=today.day)
        serializer = self.get_serializer(today_menu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
