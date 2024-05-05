"""API endpoints for team extension."""

from djangorestframework_camel_case.render import CamelCaseJSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from wagtail.api.v2.views import BaseAPIViewSet

from django.urls import path

from .filters import TeamMemberFilter
from .models import TeamMember
from .serializers import TeamMemberSerializer


class TeamAPIViewSet(BaseAPIViewSet):
    base_serializer_class = TeamMemberSerializer
    name = 'team'
    model = TeamMember
    queryset = TeamMember.objects.all()
    lookup_url_kwarg = 'pk'
    permission_classes = [IsAuthenticated]
    renderer_classes = [CamelCaseJSONRenderer]
    meta_fields = []
    filterset_class = TeamMemberFilter

    def get_serializer_class(self):
        return self.base_serializer_class

    @classmethod
    def get_urlpatterns(cls):
        return [
            path('', cls.as_view({'get': 'listing_view'}), name='listing'),
            path('<int:pk>/', cls.as_view({'get': 'detail_view'}), name='detail'),
            path('find/', cls.as_view({'get': 'find_view'}), name='find'),
        ]

    def listing_view(self, request):  # noqa: ARG002
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def detail_view(self, request, pk):  # noqa: ARG002
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_queryset(self):
        self.filterset = self.filterset_class(
            self.request.GET,
            queryset=self.queryset.order_by('name'),
        )
        return self.filterset.qs.distinct()
