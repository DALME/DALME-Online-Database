from django.contrib.auth.models import Group

from dalme_api.serializers import (AgentSerializer, ContentClassSerializer, ContentTypeSerializer,
                                   CountryReferenceSerializer, GroupSerializer, LanguageReferenceSerializer, LibraryReferenceSerializer,
                                   LocaleReferenceSerializer, PlaceSerializer, RightsPolicySerializer, SimpleAttributeSerializer)

from dalme_app.models import (Agent, Attribute, Content_class, Content_type, CountryReference,
                              LanguageReference, LibraryReference, LocaleReference, Place, RightsPolicy)

from dalme_api.access_policies import AgentAccessPolicy, GeneralAccessPolicy, RightsAccessPolicy, LibraryReferenceAccessPolicy, LocaleAccessPolicy, PlaceAccessPolicy
from ._common import DALMEBaseViewSet
from dalme_api.filters import ContenTypeFilter


class Agents(DALMEBaseViewSet):
    """ API endpoint for managing agents """
    permission_classes = (AgentAccessPolicy,)
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    filterset_fields = ['id', 'type']
    search_fields = ['id', 'standard_name', 'notes']
    ordering_fields = ['id', 'standard_name', 'type']
    ordering = ['type', 'standard_name']


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


class LibraryReferences(DALMEBaseViewSet):
    """ API endpoint for managing library references """
    permission_classes = (LibraryReferenceAccessPolicy,)
    queryset = LibraryReference.objects.all()
    serializer_class = LibraryReferenceSerializer
    filterset_fields = ['id', 'name', 'description', 'zotero_id']
    search_fields = ['id', 'name', 'description', 'zotero_id']
    ordering_fields = ['id', 'name', 'description', 'zotero_id']
    ordering = ['name']


class Locales(DALMEBaseViewSet):
    """ API endpoint for managing locales """
    permission_classes = (LocaleAccessPolicy,)
    queryset = LocaleReference.objects.all()
    serializer_class = LocaleReferenceSerializer
    filterset_fields = ['id', 'name', 'administrative_region', 'country__name']
    search_fields = ['id', 'name', 'administrative_region', 'country__name']
    ordering_fields = ['id', 'name', 'administrative_region', 'country', 'latitude', 'longitude']
    ordering = ['name']


class Places(DALMEBaseViewSet):
    """ API endpoint for managing places """
    permission_classes = (PlaceAccessPolicy,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ['id']
    search_fields = ['id', 'standard_name', 'notes', 'locale__name', 'locale__country__name']
    ordering_fields = ['id', 'standard_name', 'locale__name']
    ordering = ['locale__name', 'standard_name']


class Rights(DALMEBaseViewSet):
    """ API endpoint for managing rights policies """
    permission_classes = (RightsAccessPolicy,)
    queryset = RightsPolicy.objects.all()
    serializer_class = RightsPolicySerializer
