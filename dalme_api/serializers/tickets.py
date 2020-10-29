from dalme_app.models import Ticket
from rest_framework import serializers
from dalme_api.serializers.others import TagSerializer


class TicketSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False)
    creation_timestamp = serializers.DateTimeField(format='%d-%b-%Y@%H:%M', required=False)

    class Meta:
        model = Ticket
        fields = ('id', 'subject', 'description', 'status', 'tags', 'url', 'file',
                  'creation_user', 'creation_timestamp')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['comment_count'] = instance.comments.count()
        ticket = '<div class="d-flex align-items-center"><i class="fa fa-exclamation-circle ticket-status-{} fa-fw"></i>'.format(ret['status'])
        ticket += '<a href="/tickets/'+str(ret['id'])+'" class="ticket_subject">'+ret['subject']+'</a>'
        if ret['comment_count'] > 0:
            ticket += '<i class="fas fa-comment fa-lg icon-badge ml-2"></i><span class="icon-badge-count">{}</span></div>'.format(ret['comment_count'])
        ret['ticket'] = ticket
        attachments = ''
        if ret['url'] is not None:
            attachments += '<a href="{}" class="task-attachment">URL</a>'.format(ret['url'])
        if ret['file'] is not None:
            attachments += '<a href="/download/{}" class="task-attachment">File</a>'.format(instance.file.file)
        ret['attachments'] = attachments
        return ret
