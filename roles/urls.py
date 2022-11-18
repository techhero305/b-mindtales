from django.urls import path

from roles.views import RoleListCreateView, RoleRetrieveUpdateDeleteView

urlpatterns = [
    path('', RoleListCreateView.as_view(), name="List_Create_Role"),
    path('<int:id>/', RoleRetrieveUpdateDeleteView.as_view(), name="Retrieve_Update_Delete_Role"),
]
