"""Define API filtering logic for ticket resources."""

from django_filters import rest_framework as filters

from ida.models import Ticket


class TicketFilter(filters.FilterSet):
    """Filter for Tickets endpoint."""

    # tags = filters.CharFilter(field_name='tags__tag', lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = [
            'id',
            'subject',
            'description',
            'status',
            'url',
            'creation_user',
            'creation_timestamp',
            'assigned_to',
        ]
