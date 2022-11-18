from django.db.models import ProtectedError
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from internal_menu_selection.common_permissions import IsAuthorizedForModel, IsAuthorizedForListModel
from internal_menu_selection.pagination import CustomPagination
from roles.models import Role
from roles.serializers import RoleSerializer


class RoleRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update and delete role
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedForModel]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RoleSerializer(instance)
        try:
            instance.delete()
        except ProtectedError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


class RoleListCreateView(generics.ListCreateAPIView):
    """
    View to Add role and view list of roles
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['id', 'name', '-id', '-name']
    permission_classes = [IsAuthenticated, DjangoModelPermissions, IsAuthorizedForListModel]
