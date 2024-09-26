from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet

from ..models import Activity
from ..permissions import IsOwner
from ..serializer import ActivitySerializer


class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.filter(
        is_published=True
    ).order_by('-id').select_related('user', 'subject', 'level')
    serializer_class = ActivitySerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly, ]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', "DELETE"]:
            return [IsOwner(), ]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
