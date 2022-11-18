from django.db.models import ProtectedError
from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from internal_menu_selection.common_permissions import IsAuthorizedForListModel, IsAuthorizedForModel
from users.models import User
from users.serializers import EmployeeRegistrationSerializer, EmployeeSerializer


class EmployeeCreateView(generics.CreateAPIView):
    """
    View for register employee
    """
    queryset = User.objects.all()
    serializer_class = EmployeeRegistrationSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]


class EmployeeListView(generics.ListAPIView):
    """
    View for list of all employees
    """
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedForListModel]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['id', 'first_name', 'last_name', 'email', '-id', '-first_name', '-last_name', '-email']


class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieve, update, delete employee.
    """
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedForModel]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            instance.delete()
        except ProtectedError as err:
            return Response(str(err), status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
