from rest_framework import viewsets

from base.models import Page
from api.v1.serializers import PagesSerializer, PageDetailSerializer


class PageViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        if self.action == 'retrieve':
            return Page.objects.prefetch_related('content').all()
        else:
            return Page.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PageDetailSerializer
        else:
            return PagesSerializer
