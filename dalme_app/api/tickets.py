from rest_framework.response import Response
from rest_framework.decorators import action
from dalme_app.serializers import TicketSerializer
from dalme_app.models import Ticket
from dalme_app.access_policies import GeneralAccessPolicy
from ._common import DALMEBaseViewSet


class Tickets(DALMEBaseViewSet):
    """ API endpoint for managing issue tickets """
    permission_classes = (GeneralAccessPolicy,)
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

    @action(detail=True, methods=['patch'])
    def set_state(self, request, *args, **kwargs):
        object = self.get_object()
        try:
            action = self.request.POST['action']
            if action == 'Close':
                object.status = 1
                object.save(update_fields=['status', 'modification_user', 'modification_timestamp'])
            elif action == 'Open':
                object.status = 0
                object.save(update_fields=['status', 'modification_user', 'modification_timestamp'])
            result = {'username': self.request.user.username}
            status = 201
        except Exception as e:
            result = {'error': str(e)}
            status = 400
        return Response(result, status)
