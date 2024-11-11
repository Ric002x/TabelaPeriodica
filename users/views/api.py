from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ..permissions import IsAuthenticatedUser
from ..serializers import UsersChangePasswordSerializer, UsersSerializer


class UsersAPIViewSet(ModelViewSet):
    serializer_class = UsersSerializer
    http_method_names = ['get', 'post', 'patch', 'head', 'options']
    User = get_user_model()
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method in ['GET', 'PATCH']:
            return [IsAuthenticatedUser(), IsAuthenticated()]
        return super().get_permissions()

    def list(self, request, *args, **kwargs):
        return Response({
            'detail': 'Página não encontrada'
        }, status=status.HTTP_404_NOT_FOUND)


class UsersChangePasswordAPI(UpdateAPIView):
    serializer_class = UsersChangePasswordSerializer
    http_method_names = ['patch']
    User = get_user_model()
    queryset = User.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        if self.request.method in ['PATCH']:
            return [IsAuthenticatedUser(), IsAuthenticated()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
