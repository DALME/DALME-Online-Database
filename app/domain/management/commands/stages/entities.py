"""Fix entities."""

from datetime import date

import lxml.etree as et
import regex as re  # https://pypi.org/project/regex/
from tqdm import tqdm

from django.db import transaction
from django.db.utils import IntegrityError

from domain.models import (
    Agent,
    Attribute,
    AttributeType,
    CountryReference,
    EntityPhrase,
    LocaleReference,
    Location,
    Person,
    Record,
    Transcription,
)

from .base import BaseStage
from .fixtures import NAMED_AGENTS, NEW_LOCALES, REMOVAL_MATCHES, RS_TYPES, UNATTACHED_AGENTS


class Stage(BaseStage):
    """Data fixes for entities."""

    name = '15 Entities'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        self.fix_existing_rs_tags()
        self.delete_incorrect_data()
        self.process_named_agents()
        self.process_unattached_named_agents()
        self.create_new_locales()
        self.sync_entities_and_rs_tags()

    @transaction.atomic
    def fix_existing_rs_tags(self):
        """Fix attributes in RS tags and eliminate incorrect ones."""
        transcriptions = Transcription.objects.all()
        total = transcriptions.count()
        count_fixed = 0

        self.logger.info('Fixing RS tags...')

        for tr in tqdm(transcriptions, total=total, desc='                     completed', leave=False):
            xml_parser = et.XMLParser(recover=True)
            tree = et.fromstring('<xml>' + tr.transcription + '</xml>', xml_parser)
            entities = tree.findall('.//rs')
            if len(entities) > 0:
                changed = False
                for ent in entities:
                    typ = ent.get('type')
                    subtyp = ent.get('subtype')

                    # rs tags with type='agent' and subtype='person' -> type='person'
                    if typ == 'agent' and subtyp == 'person':
                        ent.set('type', 'person')
                        ent.attrib.pop('subtype', None)
                        changed = True

                    # rs tags without type attribute or types = location, object, material, feast day
                    # or without content -> remove tag
                    text_content = self.clean_rs_content(ent)

                    if typ in [None, 'location', 'object', 'material', 'feast day'] or text_content in REMOVAL_MATCHES:
                        self.remove_rs_entity(ent)
                        changed = True

                if changed:
                    count_fixed += 1
                    tr.transcription = et.tostring(
                        tree, encoding='utf8', xml_declaration=False, pretty_print=True
                    ).decode('utf-8')[5:-6]
                    tr.save(update_fields=['transcription'])

        self.logger.info('Fixed RS tags in %s out of %s transcriptions.', count_fixed, total)

    @transaction.atomic
    def delete_incorrect_data(self):
        """Remove incorrect/outdated data from tables."""
        self.logger.info('Removing incorrect or outdated entity data...')

        ephs = EntityPhrase.objects.all()
        total = ephs.count()
        ephs.delete()
        self.logger.info('Deleted %s EntityPhrase records.', total)

        people = Person.objects.filter(creation_timestamp__date=date(2021, 1, 30))
        total = people.count()
        people.delete()
        self.logger.info('Deleted %s Person records with date 2021-01-30.', total)

        locs = Location.objects.all()
        total = locs.count()
        locs.delete()
        self.logger.info('Deleted %s Location records.', total)

        nptype = AttributeType.objects.get(name='named_persons')
        nps = Attribute.objects.filter(attribute_type=nptype)
        total = nps.count()
        nps.delete()
        nptype.delete()
        self.logger.info('Deleted %s "named_person" attributes.', total)

    @transaction.atomic
    def process_named_agents(self):  # noqa: C901, PLR0912
        """Process named agents attached to records."""
        self.logger.info('Processing named agents...')

        atype_name = AttributeType.objects.get(name='name')
        atype_description = AttributeType.objects.get(name='description')
        count = 0

        for na in tqdm(NAMED_AGENTS, total=len(NAMED_AGENTS), desc='                     completed', leave=False):
            record_ids = na['record_id'] if isinstance(na['record_id'], list) else [na['record_id']]
            match_string = na['match']
            agent_name = na['name']
            agent_type = na['agent_type']
            agent_description = na.get('description')
            agent_alt_names = na.get('alt_names')

            for record_id in record_ids:
                record = Record.unattributed.filter(pk=record_id)
                if record.exists():
                    # i=insertions, d=deletions, s=substitutions
                    substitute = round(len(match_string) / 8)
                    insert = max(round(substitute / 2), 2)
                    delete = max(round(substitute / 2), 1)
                    fuzziness = f'i<={insert},d<={delete},s<={substitute}'
                    pattern = r'(\b' + match_string + r'\b){' + fuzziness + '}'

                    transcriptions = [
                        i.transcription for i in record.first().pagenodes.all() if i.transcription is not None
                    ]

                    if len(transcriptions) > 0:
                        for tr in transcriptions:
                            changed = False
                            xml_parser = et.XMLParser(recover=True)
                            tree = et.fromstring('<xml>' + tr.transcription + '</xml>', xml_parser)
                            find_text = et.XPath('//text()')
                            text_list = find_text(tree)
                            if len(text_list) > 0:
                                matched_str = []
                                for txt in text_list:
                                    try:
                                        match = re.search(pattern, txt, re.BESTMATCH)
                                    except TypeError:
                                        match = None
                                        self.logger.exception('Match error in %s with pattern %s.', txt, pattern)

                                    if match:
                                        # create Agent instance (if necessary)
                                        agent, created = Agent.objects.get_or_create(
                                            name=agent_name,
                                            agent_type=agent_type,
                                            defaults={
                                                'creation_user_id': 1,
                                                'modification_user_id': 1,
                                            },
                                        )

                                        if created:
                                            if agent_description:
                                                Attribute.objects.create(
                                                    content_object=agent,
                                                    attribute_type=atype_description,
                                                    value=agent_description,
                                                    creation_user_id=1,
                                                    modification_user_id=1,
                                                )

                                            if agent_alt_names:
                                                for alt_name in agent_alt_names:
                                                    Attribute.objects.create(
                                                        content_object=agent,
                                                        attribute_type=atype_name,
                                                        value=alt_name,
                                                        creation_user_id=1,
                                                        modification_user_id=1,
                                                    )

                                        # create EntityPhrase instance
                                        ep_instance = EntityPhrase.objects.create(
                                            transcription=tr,
                                            content_object=agent,
                                            creation_user_id=1,
                                            modification_user_id=1,
                                        )

                                        matched_str.append(match.group(0))

                                        self.process_agent_element(txt, match, agent_type, ep_instance.id)
                                        changed = True
                                        count += 1

                            if changed:
                                tr.transcription = et.tostring(
                                    tree, encoding='utf8', xml_declaration=False, pretty_print=True
                                ).decode('utf-8')[5:-6]
                                tr.save(update_fields=['transcription'])

        self.logger.info('Processed %s named agents.', count)

    @transaction.atomic
    def process_unattached_named_agents(self):  # noqa: C901, PLR0912, PLR0915
        """Process unattached named agents (i.e. those not mentioned directly in the text)."""
        self.logger.info('Processing unattached named agents...')

        atype_name = AttributeType.objects.get(name='name')
        atype_description = AttributeType.objects.get(name='description')
        issues = []

        for na in tqdm(
            UNATTACHED_AGENTS, total=len(UNATTACHED_AGENTS), desc='                     completed', leave=False
        ):
            record_ids = na['record_id'] if isinstance(na['record_id'], list) else [na['record_id']]
            agent_name = na['name']
            agent_type = na['agent_type']
            agent_description = na.get('description')
            agent_alt_names = na.get('alt_names')

            for record_id in record_ids:
                record = Record.unattributed.filter(pk=record_id)
                if record.exists():
                    transcriptions = [
                        i.transcription for i in record.first().pagenodes.all() if i.transcription is not None
                    ]
                    if len(transcriptions) > 0:
                        target = transcriptions[0]
                        xml_parser = et.XMLParser(recover=True)
                        tree = et.fromstring('<xml>' + target.transcription + '</xml>', xml_parser)
                        rs_type = RS_TYPES[agent_type]

                        # create Agent instance (if necessary)
                        agent, created = Agent.objects.get_or_create(
                            name=agent_name,
                            agent_type=agent_type,
                            defaults={
                                'creation_user_id': 1,
                                'modification_user_id': 1,
                            },
                        )

                        if created:
                            if agent_description:
                                Attribute.objects.create(
                                    content_object=agent,
                                    attribute_type=atype_description,
                                    value=agent_description,
                                    creation_user_id=1,
                                    modification_user_id=1,
                                )

                            if agent_alt_names:
                                for alt_name in agent_alt_names:
                                    Attribute.objects.create(
                                        content_object=agent,
                                        attribute_type=atype_name,
                                        value=alt_name,
                                        creation_user_id=1,
                                        modification_user_id=1,
                                    )

                        # create EntityPhrase instance
                        ep_instance = EntityPhrase.objects.create(
                            transcription=target,
                            content_object=agent,
                            creation_user_id=1,
                            modification_user_id=1,
                        )

                        # check if there's already a mute tag for named agents
                        mute_wrapper = tree.find('.//mute[@type="named_agents_wrapper"]')
                        if mute_wrapper is not None:
                            # add RS tag for agent
                            new_agent = et.SubElement(mute_wrapper, 'rs', type=rs_type, key=str(ep_instance.id))
                            new_agent.text = agent_name
                            new_agent.tail = '\n'

                        else:
                            # add line breaks at the end
                            elements = tree.getchildren()
                            if len(elements) > 0:
                                last_el = elements[-1]
                                last_el_tail = last_el.tail if last_el.tail else ''
                                last_el.tail = last_el_tail + '\n\n'
                            elif tree.text:
                                tree.text = tree.text + '\n\n'
                            else:
                                tree.text = '\n\n'
                                issues.append(f'Transcription {target.id} has no content.')

                            # create mute tag
                            mute_wrapper = et.SubElement(tree, 'mute', type='named_agents_wrapper')
                            mute_wrapper.text = '\n'
                            # add RS tag for agent
                            new_agent = et.SubElement(mute_wrapper, 'rs', type=rs_type, key=str(ep_instance.id))
                            new_agent.text = agent_name
                            new_agent.tail = '\n'
                            mute_wrapper.tail = '\n\n'

                        target.transcription = et.tostring(
                            tree, encoding='utf8', xml_declaration=False, pretty_print=True
                        ).decode('utf-8')[5:-6]
                        target.save(update_fields=['transcription'])

        if len(issues) > 0:
            for issue in issues:
                self.logger.warning(issue)

        self.logger.info('Processed %s unattached named agents.', len(UNATTACHED_AGENTS))

    @transaction.atomic
    def create_new_locales(self):
        """Create new locales to be used with place entities."""
        self.logger.info('Creating new locales...')

        italy = CountryReference.objects.get(name='Italy')
        count = 0

        for locale in NEW_LOCALES:
            locale['country'] = italy
            locale['defaults'] = {
                'creation_user_id': 1,
                'modification_user_id': 1,
            }
            try:
                LocaleReference.objects.get_or_create(**locale)
                count += 1
            except IntegrityError:
                self.logger.exception('Failed to create locale: %s.', locale)

        self.logger.info('Created %s new locales.', count)

    @transaction.atomic
    def sync_entities_and_rs_tags(self):  # noqa: C901, PLR0912, PLR0915
        """Synchronize entities and RS tags."""
        self.logger.info('Synchronizing entities and RS tags...')

        transcriptions = Transcription.objects.all()
        total = transcriptions.count()
        count_fixed = 0

        for tr in tqdm(transcriptions, total=total, desc='                     completed', leave=False):
            changed = False
            xml_parser = et.XMLParser(recover=True)
            tree = et.fromstring('<xml>' + tr.transcription + '</xml>', xml_parser)
            entities = tree.findall('.//rs')
            if len(entities) > 0:
                for ent in entities:
                    typ = ent.get('type')
                    key = ent.get('key')

                    # skip if this is one of the new additions
                    if key and len(key) == 36 and EntityPhrase.objects.filter(pk=key).exists():  # noqa: PLR2004
                        continue

                    content = self.clean_rs_content(ent)

                    if content is None:
                        self.remove_rs_entity(ent)
                        changed = True
                        continue

                    if typ == 'person':
                        name, is_org = self.get_agent_name(content)
                        if name is None:
                            self.remove_rs_entity(ent)
                            changed = True
                            continue

                        ep_id = self.create_phrase(
                            tr,
                            'agent',
                            {'name': name, 'agent_type': 2 if is_org else 1},
                        )

                        # update rs tag
                        if is_org:
                            ent.set('type', 'organization')

                        ent.set('key', ep_id)

                        changed = True

                    elif typ == 'organization':
                        name = self.clean_org_name(content)

                        ep_id = self.create_phrase(
                            tr,
                            'agent',
                            {'name': name, 'agent_type': 2},
                        )

                        ent.set('key', ep_id)  # update key

                        changed = True

                    elif typ == 'place':
                        name = self.get_placename(content)
                        if name is None:
                            self.remove_rs_entity(ent)
                            changed = True
                            continue

                        ep_id = self.create_phrase(
                            tr,
                            'place',
                            {'name': name},
                        )

                        ent.set('key', ep_id)  # update key

                        changed = True

                    elif typ == 'locus':
                        if not self.check_locus(content):
                            self.remove_rs_entity(ent)
                            changed = True
                            continue

                        ep_id = self.create_phrase(tr, 'locus')
                        ent.set('key', ep_id)  # update key
                        changed = True

            if changed:
                count_fixed += 1
                tr.transcription = et.tostring(tree, encoding='utf8', xml_declaration=False, pretty_print=True).decode(
                    'utf-8'
                )[5:-6]
                tr.save(update_fields=['transcription'])

        self.logger.info('Synchronized tags in %s out of %s transcriptions.', count_fixed, total)
