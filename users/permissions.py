from rest_framework.permissions import BasePermission


class IsAuthenticatedUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Compara o username do objeto com o username do usuário autenticado
        return hasattr(obj, 'username') and obj \
            .username == request.user.username
