"""Process named agents."""

from django.db import transaction

from domain.models import (
    Attribute,
    AttributeType,
    EntityPhrase,
    Organization,
    Person,
    Record,
)

from .base import BaseStage
from .fixtures import NAMED_AGENTS


class Stage(BaseStage):
    """Data processing stage for named agents."""

    name = '10 Named Agents'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.remove_named_persons()
        self.process_named_agents()

    @transaction.atomic
    def remove_named_persons(self):
        self.logger.info('Removing named persons...')
        atype = AttributeType.objects.get(name='named_persons')
        Attribute.objects.filter(attribute_type=atype).delete()
        self.logger.info('Attributes removed.')
        atype.delete()
        self.logger.info('Attribute type deleted.')

    @transaction.atomic
    def process_named_agents(self):
        self.logger.info('Processing named agents')

        for entry in NAMED_AGENTS:
            record_ids = entry['record_id']
            record_ids = record_ids if isinstance(record_ids, list) else [record_ids]
            name = entry['name']
            tr_ids = []
            for rec_id in record_ids:
                try:
                    record = Record.objects.get(pk=rec_id)
                    if record.has_transcriptions:
                        page_nodes = record.pagenodes.all().select_related('transcription')
                        for node in page_nodes:
                            if node.transcription and name in node.transcription.text_blob:
                                tr_ids.append(node.transcription.id)
                except Record.DoesNotExist:
                    self.logger.error('Record %s not found.', rec_id)  # noqa: TRY400
            if tr_ids:
                agent_type = entry['agent_type']
                agent_model = Person if agent_type == 1 else Organization
                agent = agent_model.objects.create(
                    name=name,
                    agent_type=agent_type,
                    creation_user_id=1,
                    modification_user_id=1,
                )
                for tr_id in tr_ids:
                    EntityPhrase.objects.create(
                        transcription_id=tr_id,
                        content_object=agent,
                        creation_user_id=1,
                        modification_user_id=1,
                    )
