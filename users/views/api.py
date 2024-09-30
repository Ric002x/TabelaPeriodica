from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet

from ..serializers import UsersSerializer


class UsersAPISet(ReadOnlyModelViewSet):
    serializer_class = UsersSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(
            username=self.request.user.username)  # type:ignore
        return qs
