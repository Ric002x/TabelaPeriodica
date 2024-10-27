from rest_framework.generics import ListAPIView, RetrieveAPIView

from ..models import Element
from ..serializer import ElementDetailSerializer, ElementsSerializer


class ElementListViewAPI(ListAPIView):
    queryset = Element.objects.order_by('id').all()
    serializer_class = ElementsSerializer
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ElementDetailViewAPI(RetrieveAPIView):
    queryset = Element.objects.order_by('id').all()
    serializer_class = ElementDetailSerializer
    lookup_field = 'slug'
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
