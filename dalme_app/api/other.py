from django.contrib.auth.models import Group
from django_celery_results.models import TaskResult

from dalme_app.serializers import (AgentSerializer, AsyncTaskSerializer, ContentClassSerializer, ContentTypeSerializer,
                                   CountryReferenceSerializer, GroupSerializer, LanguageReferenceSerializer,
                                   LocaleReferenceSerializer, RightsPolicySerializer, SimpleAttributeSerializer)

from dalme_app.models import (Agent, Attribute, Content_class, Content_type, CountryReference,
                              LanguageReference, LocaleReference, RightsPolicy)

from dalme_app.access_policies import GeneralAccessPolicy, RightsAccessPolicy
from ._common import DALMEBaseViewSet
from dalme_app.filters import ContenTypeFilter


class Agents(DALMEBaseViewSet):
    """ API endpoint for managing agents """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filterset_fields = ['id', 'type']
    search_fields = ['id', 'standard_name', 'notes']
    ordering_fields = ['id', 'standard_name', 'type']
    ordering = ['type', 'standard_name']


class AsynchronousTasks(DALMEBaseViewSet):
    """ API endpoint for managing asynchronous tasks """
    permission_classes = (GeneralAccessPolicy,)
    queryset = TaskResult.objects.all()
    serializer_class = AsyncTaskSerializer
    filterset_fields = ['id', 'status', 'result']
    search_fields = ['id', 'task_name', 'result', 'traceback']
    ordering_fields = ['id', 'task_name', 'status', 'date_done', 'result', 'traceback']
    ordering = ['id']


class Attributes(DALMEBaseViewSet):
    """ API endpoint for managing attributes """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Attribute.objects.all().order_by('attribute_type')
    serializer_class = SimpleAttributeSerializer


class ContentClasses(DALMEBaseViewSet):
    """ API endpoint for managing content classes """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Content_class.objects.all()
    serializer_class = ContentClassSerializer


class ContentTypes(DALMEBaseViewSet):
    """ API endpoint for managing content types """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Content_type.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContenTypeFilter


class Countries(DALMEBaseViewSet):
    """ API endpoint for managing countries """
    permission_classes = (GeneralAccessPolicy,)
    queryset = CountryReference.objects.all()
    serializer_class = CountryReferenceSerializer
    filterset_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    search_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    ordering_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    ordering = ['name']


class Groups(DALMEBaseViewSet):
    """ API endpoint for managing user groups """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ['id', 'name', 'properties__type']
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name']


class Languages(DALMEBaseViewSet):
    """ API endpoint for managing languages """
    permission_classes = (GeneralAccessPolicy,)
    queryset = LanguageReference.objects.all()
    serializer_class = LanguageReferenceSerializer
    filterset_fields = ['id', 'name', 'type', 'parent__name', 'iso6393', 'glottocode']
    search_fields = ['id', 'name', 'type', 'parent__name', 'iso6393', 'glottocode']
    ordering_fields = ['id', 'name', 'type', 'parent', 'iso6393', 'glottocode']
    ordering = ['name']


class Locales(DALMEBaseViewSet):
    """ API endpoint for managing locales """
    permission_classes = (GeneralAccessPolicy,)
    queryset = LocaleReference.objects.all()
    serializer_class = LocaleReferenceSerializer
    filterset_fields = ['id', 'name', 'administrative_region', 'country__name']
    search_fields = ['id', 'name', 'administrative_region', 'country__name']
    ordering_fields = ['id', 'name', 'administrative_region', 'country']
    ordering = ['name']


class Rights(DALMEBaseViewSet):
    """ API endpoint for managing rights policies """
    permission_classes = (RightsAccessPolicy,)
    queryset = RightsPolicy.objects.all()
    serializer_class = RightsPolicySerializer
