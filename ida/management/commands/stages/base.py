"""Base class for a data migration stage."""

import abc
import copy
import functools
import json
import re
import uuid

import markdown
import structlog
from bs4 import BeautifulSoup
from django_tenants.utils import schema_context

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import connection

from ida.models import SavedSearch, User

logger = structlog.get_logger(__name__)

REFERENCE_HREF = re.compile(r'(?:(?:http|https)://dalme.org)?/?/project/bibliography/#([A-Z0-9]{8})')

# Here are some useful statements if you want to compare ContentType diffs.
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model;
# SELECT * FROM public.django_content_type new_ct INNER JOIN restore.django_content_type old_ct ON new_ct.model = old_ct.model
# WHERE new_ct.app_label != old_ct.app_label;
ALTERED_MODEL_MAP = {
    ('core', 'agent'): 'ida.agent',
    ('core', 'attribute_type'): 'ida.attributetype',
    ('core', 'concept'): 'ida.concept',
    ('core', 'content_type'): 'ida.contenttypeextended',
    ('core', 'countryreference'): 'ida.countryreference',
    ('core', 'entity_phrase'): 'ida.entityphrase',
    ('core', 'headword'): 'ida.headword',
    ('core', 'object'): 'ida.object',
    ('core', 'object_attribute'): 'ida.objectattribute',
    ('core', 'page'): 'ida.page',
    ('core', 'place'): 'ida.place',
    ('core', 'set'): 'ida.collection',
    ('core', 'set_x_content'): 'ida.collectionmembership',
    ('core', 'source'): 'ida.record',
    ('core', 'source_credit'): 'ida.relationship',
    ('core', 'source_pages'): 'ida.pagenode',
    ('core', 'ticket'): 'ida.ticket',
    ('core', 'token'): 'ida.token',
    ('core', 'transcription'): 'ida.transcription',
    ('core', 'wordform'): 'ida.wordform',
    ('core', 'work_log'): 'ida.worklog',
    ('core', 'work_flow'): 'ida.workflow',
    ('core', 'task'): 'ida.task',
    ('core', 'tasklist'): 'ida.tasklist',
    ('core', 'comment'): 'ida.comment',
    ('core', 'collection'): 'ida.collection',
    ('core', 'collectionmembership'): 'ida.collectionmembership',
    ('core', 'attachment'): 'ida.attachment',
    ('core', 'savedsearch'): 'ida.savedsearch',
    ('core', 'tag'): 'ida.tag',
    ('public', 'dalmeimage'): 'publicimages.baseimage',
}

SOURCES_MODEL_MAP = {
    1: ('ida', 'publication'),
    2: ('ida', 'publication'),
    3: ('ida', 'publication'),
    4: ('ida', 'publication'),
    5: ('ida', 'publication'),
    6: ('ida', 'publication'),
    7: ('ida', 'publication'),
    8: ('ida', 'publication'),
    9: ('ida', 'publication'),
    10: ('ida', 'publication'),
    11: ('ida', 'publication'),
    12: ('ida', 'recordgroup'),
    19: ('ida', 'organization'),
}

REF_CITATIONS = {
    '6YDI5HL6': '(Smith, 2020)',
    'WJLVYXYP': '(Sibon, 2011)',
    'LYJR5IHM': '(Coulet, 2004)',
    'TS749RWH': '(Baratier, 1961)',
    '6NUFKTEG': '(Mély & Bishop, 1892)',
    'F2FFVVX8': '(Volkert, 1982)',
    '3GJ5F9HJ': '(Coulet, 2004)',
    'ER34URS8': '(Le Roux de Lincy, 1846)',
    '5QK2S98X': '(Barnel, 1999)',
    'L9ALQFNF': '(Ripert, Barnel, Bresc, Herbeth, & Colin, 1993)',
    'BZ53KGMW': '(Stouff, 1996)',
    'IFRJ2YQ6': '(Smail, Pizzorno, & Hay, 2020)',
    'UH5EUVZC': '(Villard, 1907)',
    'NY7H8NIH': '(Ferrand, 2017)',
    'DBB2IVEC': '(Livi, 1928)',
    'SA6QKDAR': '(Longhi, 2020)',
    'YX4Y4RRJ': '(Barry, 1898)',
    'XAQBR8XE': '(Teaching Medieval Slavery and Captivity, n.d.)',
    'VZQ5BBTG': '(Origo, 1955)',
    'JHH4LIGY': '(Fernandes, Liberato, Marques, & Cunha, 2017)',
    '6VZUI7JY': '(Oliver, 2016)',
    'ZZXGLVMZ': '(Rigaud, 1996)',
    'ZUMTQ5B9': '(Reitzel, 1980)',
    '2RUWVY7B': '(Howell, 1996)',
    'SNB4JFJ9': '(Braun, 1907)',
    'SBBLYP96': '(Davril, Thibodeau, & Guyot, 1995)',
    'TNEXXNIQ': '(Braun, 1937)',
    'UCVN8LWL': '(Miller, 2014)',
    'TQVX23W6': '(Berthod, 2001)',
    'QZNHF7Q3': '(Piponnier, 1989)',
    'Q62RN9ND': '(Fircks, 2018)',
    'TBIJ9DYD': '(Deregnaucourt, 1981)',
    'J9BYMBP2': '(Deregnaucourt, 1982)',
    'Y44RIA8Q': '(Mane & Piponnier, 1992)',
    'XL9F9RTZ': '(Carroll-Clark, 2005)',
    'MJWEGUKG': '(Blaschitz, Hundsbichler, Jaritz, & Vavra, 1992)',
    'XXD7JM9D': '(Baumgarten, 2014)',
}

USER_NAME_CONCORDANCE = {
    'Anne E. Lester': 'Anne Lester',
    'Juan Vicente García Marsilla': 'Juan-Vicente Garcia Marsilla',
    'Juliette Calvarin': 'Jules Calvarin',
    'Pablo Sanahuja Ferrer': 'Pablo Sanahuja',
}


class MigrationError(Exception):
    """Raise this exception anywhere within a stage to abort the transaction."""


class BaseStage(abc.ABC):
    """Interface for a data migration stage."""

    FN_REGISTER = {}  # register to keep track of footnote indices
    FOOTNOTES = []  # storage for footnotes

    @abc.abstractmethod
    def apply(self):
        """Execute the migration stage."""
        ...

    @property
    def logger(self):
        """Provide the logger to all inheriting classes."""
        return logger

    @functools.cached_property
    def old_content_types_index(self):
        """Index the content types from the data being migrated."""
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM restore.django_content_type')
            rows = self.map_rows(cursor)

            index = {}
            for ct in rows:
                if (ct['app_label'], ct['model']) in ALTERED_MODEL_MAP:
                    # Let's just update these on the fly to the new values and
                    # it reduces the overall complexity of the transformation.
                    app_label, model = ALTERED_MODEL_MAP[(ct['app_label'], ct['model'])].split('.')
                else:
                    app_label, model = (ct['app_label'], ct['model'])

                ct_id = ct['id']
                # Return the data as the key into the new_cts index.
                index[ct_id] = (app_label, model)

            return index

    @functools.cached_property
    def old_permissions_index(self):
        """Index the permissions from the data being migrated."""
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM restore.auth_permission')
            rows = self.map_rows(cursor)
        return {row['id']: (row['codename'], row['content_type_id']) for row in rows}

    @functools.cached_property
    def new_content_types_index(self):
        """Index the content types from the current db state."""
        index = {}
        for ct in ContentType.objects.all():
            app_label = ct.app_label
            model = ct.model
            key = (app_label, model)
            index[key] = {'id': ct.id, 'model': model, 'app_label': app_label}

        return index

    @staticmethod
    def map_rows(cursor):
        """Map db rows from tuples to dictionaries."""
        columns = [col[0] for col in cursor.description]
        return (dict(zip(columns, row, strict=True)) for row in cursor.fetchall())

    @staticmethod
    def get_fields_by_type(model, field_types, as_map=False):
        # Wagtail subclasses Django fields without redefining the method
        # or declaring the __name__ attribute
        # so for certain types we need to use the field's class instead
        # of calling field.get_internal_type()
        filter_by_class = ['RichTextField']

        if not isinstance(field_types, list):
            field_types = [field_types]

        target_types = [t for t in field_types if t not in filter_by_class]
        target_classes = [t for t in field_types if t in filter_by_class]

        fields = {}
        for field in model._meta.get_fields():  # noqa: SLF001
            try:
                field_cls_name = str(field.__class__)[8:-2].split('.')[-1]
                if field.get_internal_type() in target_types or field_cls_name in target_classes:
                    fields[field.name] = field.get_internal_type()
            except AttributeError:  # it's a GenericForeignKey
                continue
        return fields if as_map else list(fields.keys())

    def map_content_type(self, old_id, id_only=False):
        """Map an old content type to a new content type."""
        if not old_id:
            return None
        if id_only and old_id in SOURCES_MODEL_MAP:
            key = SOURCES_MODEL_MAP[old_id]
            return self.new_content_types_index[key]['id']
        key = self.old_content_types_index[old_id]
        if id_only:
            return self.new_content_types_index[key]['id']
        return self.new_content_types_index[key]

    def map_permissions(self, old_id):
        auth_permission = apps.get_model(app_label='auth', model_name='permission')
        codename, old_ctype = self.old_permissions_index[old_id]
        target_ctype = self.map_content_type(old_ctype, id_only=True)
        return auth_permission.objects.get(codename=codename, content_type_id=target_ctype).id

    def clean_db_value(self, value, field_type):
        if value is None:
            return 'null'
        if field_type == 'JSONField':
            return f'$${value}$$::jsonb'
        if field_type in ['AutoField', 'BigAutoField', 'BigIntegerField', 'IntegerField']:
            return value if isinstance(value, int) else int(value)
        return f'$${value}$$'

    def markdown_to_html(self, content):
        # <span data-footnote=\"For Bons-Enfants, houses of poor grammar-school students attested across northern France and francophone Flanders (as Douai),
        # Joan M. Reitzel, &quot;[The Medieval House of Bons-Enfants](http://dalme.org/project/bibliography/#ZUMTQ5B9),&quot; _Viator_ 11 (1980): 179-207.\"
        # data-note_id=\"1fe36ff5-2e03-4890-82b1-71090d6333d7\">✱</span>
        soup = BeautifulSoup(markdown.markdown(content), features='lxml')
        references = soup.find_all('a', href=REFERENCE_HREF)
        if references:
            soup = self.convert_references(soup)

        return ''.join(str(b) for b in soup.body.findChildren(recursive=False))

    def convert_references(self, soup):
        for ref in soup.find_all('a', href=REFERENCE_HREF):
            # format: <a data-biblio="54" data-id="R476GUY2" data-reference="(Telliez, 2011)" linktype="reference">consumption</a>
            match = REFERENCE_HREF.fullmatch(ref['href'])
            if match:
                ref['data-biblio'] = self.biblio_page_id
                ref_id = match.group(1)
                try:
                    citation = REF_CITATIONS[ref_id]
                except KeyError:
                    citation = ''
                    self.logger.info('Reference id: %s not in citation list!', ref_id)
                ref['data-id'] = ref_id
                ref['data-reference'] = citation  # TODO: figure out a better way to get the citation!
                ref['linktype'] = 'reference'
                del ref['href']

        return soup

    def get_footnote_id(self, content, page_id):
        if self.FOOTNOTES:
            results = [i for i in self.FOOTNOTES if i['text'] == content and i['page_id'] == page_id]
            if results and len(results) == 1:
                return results[0]['id']
        return None

    def fix_entities(self, text, page_id, is_rev=False):
        soup = BeautifulSoup(text, features='lxml')

        # references
        references = soup.find_all('a', href=REFERENCE_HREF)
        if references:
            soup = self.convert_references(soup)

        # footnotes
        footnotes = soup.find_all('span', attrs={'data-footnote': True})
        if footnotes:
            fn_index = self.FN_REGISTER.get(page_id, 1)

            for idx, fn in enumerate(footnotes, start=fn_index):
                # format: <a data-footnote="c847f9da-3780-4085-9426-73e7a0228b3d" linktype="footnote">✱</a>
                fn_content = self.markdown_to_html(fn['data-footnote'])

                if is_rev:
                    # we don't create footnote records for page revisions as they would be repeats
                    # of notes that already exist in the live pages
                    fn_id = self.get_footnote_id(fn_content, page_id)
                    fn['data-footnote'] = fn_id if fn_id else True

                else:
                    new_footnote_id = uuid.uuid4()
                    self.FOOTNOTES.append(
                        {
                            'id': new_footnote_id,
                            'page_id': page_id,
                            'text': fn_content,
                            'sort_order': idx,
                        }
                    )

                    fn['data-footnote'] = new_footnote_id

                self.FN_REGISTER[page_id] = idx  # update footnote index for page with last used one
                fn.name = 'a'
                fn['linktype'] = 'footnote'
                del fn['data-note_id']

            self.FN_REGISTER[page_id] += 1  # increment last index by one for next run

        # saved searches
        # source format: <a id="01d5187e-2752-466e-9e7d-64e51051facd" linktype="saved_search">storage</a>
        # target format: <a id="01d5187e-2752-466e-9e7d-64e51051facd" data-saved-search="pansier" linktype="saved_search">dissemination</a>
        saved_searches = soup.find_all('a', attrs={'linktype': 'saved_search'})
        if saved_searches:
            for ss in saved_searches:
                try:
                    search_obj = SavedSearch.objects.get(pk=ss['id'])
                    ss['data-saved-search'] = search_obj.name
                except:  # noqa: E722
                    self.logger.info('Failed to migrate saved search entity in page %s', page_id)

        return ''.join(str(b) for b in soup.body.findChildren(recursive=False))

    def parse_streamfield(self, content, page_id, is_rev=False):  # noqa: C901, PLR0912, PLR0915
        """We parse streamfields to convert between content formats and convert the old subsection blocks into the new nested system."""
        new_content = []
        subsection = None
        nested_subsection = None
        for sblock in content:
            block = copy.deepcopy(sblock)
            if not isinstance(block, str) and block.get('type') in ['subsection', 'subsection_end_marker']:
                if block.get('value', {}).get('minor_heading'):
                    block['type'] = 'nested_subsection'
                    if nested_subsection is None:
                        nested_subsection = block
                    else:
                        if subsection:
                            if not subsection['value'].get('body'):
                                subsection['value']['body'] = [nested_subsection]
                            else:
                                subsection['value']['body'].append(nested_subsection)
                        else:
                            new_content.append(nested_subsection)
                        nested_subsection = block
                else:
                    if nested_subsection:
                        if subsection:
                            if not subsection['value'].get('body'):
                                subsection['value']['body'] = [nested_subsection]
                            else:
                                subsection['value']['body'].append(nested_subsection)
                        else:
                            new_content.append(nested_subsection)

                        nested_subsection = None

                    if subsection:
                        new_content.append(subsection)

                    subsection = block if block.get('type') == 'subsection' else None
            else:
                if isinstance(block, str):
                    pass
                elif block.get('type') == 'text' and block.get('value'):
                    block['value'] = self.fix_entities(block['value'], page_id, is_rev=is_rev)

                elif block.get('type') == 'inline_image':
                    if isinstance(block['value'], dict):
                        block['value']['use_file_caption'] = not block['value'].get('show_caption')
                    else:
                        self.logger.info('Found inline image with int value: %s', block['value'])

                elif block.get('type') == 'main_image':
                    block['type'] = 'inline_image'
                    image_id = block['value']
                    block['value'] = {
                        'image': image_id,
                        'show_caption': True,
                        'use_file_caption': True,
                        'alignment': 'main',
                    }

                if nested_subsection:
                    if not nested_subsection['value'].get('body'):
                        nested_subsection['value']['body'] = [block]
                    else:
                        nested_subsection['value']['body'].append(block)

                elif subsection:
                    if not subsection['value'].get('body'):
                        subsection['value']['body'] = [block]
                    else:
                        subsection['value']['body'].append(block)

                else:
                    new_content.append(block)

        if nested_subsection:
            if subsection:
                if not subsection['value'].get('body'):
                    subsection['value']['body'] = [nested_subsection]
                else:
                    subsection['value']['body'].append(nested_subsection)
            else:
                new_content.append(nested_subsection)

        if subsection:
            new_content.append(subsection)

        return new_content

    def process_content_field(self, field_value, field_type, page_id, is_rev):
        if field_type == 'JSONField':
            field_value_json = json.loads(field_value)
            content = field_value_json['body'] if is_rev else field_value_json
            new_content = self.parse_streamfield(content, page_id, is_rev=is_rev)

            if is_rev:
                field_value_json['body'] = new_content
                field_value = json.dumps(field_value_json)
            else:
                field_value = json.dumps(new_content)

        else:
            field_value = self.fix_entities(field_value, page_id)

        return field_value

    @functools.cached_property
    def biblio_page_id(self):
        with schema_context('dalme'):
            from public.models import Bibliography

            return Bibliography.objects.first().page_ptr_id

    def user_match(self, name):
        name = USER_NAME_CONCORDANCE.get(name, name)
        match = User.objects.filter(full_name=name)
        if match.exists():
            if match.count() != 1:
                self.logger.info('Name %s matches multiple users.', name)
            else:
                return match.get()
        return None
