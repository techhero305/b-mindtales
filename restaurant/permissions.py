from rest_framework.permissions import DjangoModelPermissions


class IsOwner(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsRestaurantOwner(DjangoModelPermissions):
    def has_object_permission(self, request, view, obj):
        return obj.restaurant.owner == request.user
