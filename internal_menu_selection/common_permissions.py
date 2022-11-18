from rest_framework.permissions import DjangoModelPermissions, DjangoObjectPermissions

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class IsAuthorizedForModel(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }


class IsAuthorizedForListModel(DjangoObjectPermissions):
    def has_permission(self, request, view):
        if request.method == 'GET':
            queryset = self._queryset(view)
            app_label = queryset.model._meta.app_label
            model_name = queryset.model._meta.model_name
            perm = f'list_{model_name}'
            return bool(request.user.has_perm(f"{app_label}.{perm}"))
        else:
            return True




