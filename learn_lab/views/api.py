from rest_framework.generics import ListAPIView
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
    http_method_names = ["get", "options", "head", "patch", "post", "delete"]

    def get_permissions(self):
        if self.request.method in ['PATCH', "DELETE"]:
            return [IsOwner(), ]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ActivitiesSubjectListAPIv2(ListAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        subject_id = self.kwargs.get('pk')
        queryset = Activity.objects.filter(
            is_published=True,
            subject=subject_id).order_by(
            '-id').select_related('user', 'subject', 'level')
        return queryset


class ActivitiesLevelListAPIv2(ListAPIView):
    serializer_class = ActivitySerializer

    def get_queryset(self):
        level_id = self.kwargs.get('pk')
        queryset = Activity.objects.filter(
            is_published=True,
            level=level_id).order_by(
            '-id').select_related('user', 'subject', 'level')
        return queryset
