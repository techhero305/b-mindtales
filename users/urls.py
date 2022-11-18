from django.urls import path

from users.views import EmployeeCreateView, EmployeeListView, EmployeeRetrieveUpdateDeleteView

urlpatterns = [
    path('register/', EmployeeCreateView.as_view(), name="register_employee"),
    path('', EmployeeListView.as_view(), name="list_employee"),
    path('<int:id>/', EmployeeRetrieveUpdateDeleteView.as_view(),
         name="retrieve_update_delete_employee"),
]
