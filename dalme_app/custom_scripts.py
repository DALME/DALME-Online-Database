"""Contains general purpose scripts."""
import json
import os
import re
from datetime import date

import pandas as pd
from geopy.geocoders import AlgoliaPlaces

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from dalme_app.models import (
    Attribute,
    AttributeReference,
    Language,
    LocaleReference,
    Page,
    PublicRegister,
    Set,
    Set_x_content,
    Source,
    Transcription,
)


def get_script_menu():
    script_register = [
        {
            'name': 'session_info',
            'description': 'Outputs the contents of the current session.',
            'type': 'info',
        },
        {
            'name': 'update_folios_in_dam',
            'description': "Updates the contents of the 'folio' field in the DAM to match the value in the corresponding DALME page.",
            'type': 'danger',
        },
        {
            'name': 'rebuild_search_index',
            'description': 'Rebuilds the ElasticSearch indices.',
            'type': 'danger',
        },
        {
            'name': 'add_to_public_register',
            'description': 'Add sources marked as public to Public Register (purl endpoint).',
            'type': 'danger',
        },
        {
            'name': 'geolocate_locales',
            'description': 'Add latitude and longitude to locales.',
            'type': 'warning',
        },
        {
            'name': 'remove_11600',
            'description': 'Removes dam_id from pages for which the current value is 11600',
            'type': 'danger',
        },
        {
            'name': 'test_expression',
            'description': "Tests a simple expression that doesn't require complex data or context from the rest of the application.",
            'type': 'info',
        },
        {
            'name': 'test_django_q',
            'description': 'Tests the tasks backend.',
            'type': 'info',
        },
    ]
    _output = ''
    for item in script_register:
        _output += get_script_menu_item(**item)
    return [_output]


def get_script_menu_item(name=None, description=None, item_type=None):
    icon_dict = {
        'info': 'fa-info-circle',
        'danger': 'fa-hand-paper',
        'warning': 'fa-exclamation-triangle',
        'secondary': 'fa-scroll',
        'success': 'thumbs-up',
    }
    item = '<a class="script-item d-flex text-dark-gray" href="/tools/scripts?s={}">'
    item += f'<div class="script-icon bg-{name}-soft">'
    item += f'<i class="fas {item_type} text-{icon_dict[item_type]}"></i></div>'
    item += f'<span class="font-weight-bold mr-1">{name}: </span> {description}</a>'
    return item


def queryset_gen(search_qs):
    for item in search_qs:
        yield item.object  # This is the line that gets the model instance out of the Search object


def create_json_field_reps(request):  # noqa: ARG001
    path = os.path.join(
        'dalme_app',
        'config',
        'datatables',
        'field_defs',
        'sources.json',
    )
    with open(path) as f:
        data = json.load(f)

    for field in data:
        path = os.path.join(
            'dalme_app',
            'config',
            'datatables',
            'field_defs',
            'sources',
            '_' + field['name'] + '.json',
        )
        with open(path, 'w') as json_file:
            json_file.write(json.dumps(field, indent=4))

    return 'done'


def add_attribute_types():
    schema = []
    try:
        entries = []
        for i in schema:
            new_entry = AttributeReference()
            new_entry.name = i['Label']
            new_entry.short_name = i['Short Name']
            new_entry.data_type = 'STR'
            new_entry.source = i['URI']
            new_entry.description = i['Definition']
            new_entry.term_type = i['Type of Term']
            if 'Comment' in i:
                new_entry.notes = i['Comment']
            entries.append(new_entry)
        AttributeReference.objects.bulk_create(entries)
        result = 'Cool!'
    except Exception as e:  # noqa: BLE001
        result = 'Oops!' + str(e)

    return result


def session_info(request):
    return request.session


# def test_django_q(request):
#     async_task('dalme_app.tasks.test_task', request.user.id, task_name='test_task', hook='dalme_app.utils.send_message')
#
#
# def update_folios_in_dam(request):
#     async_task('dalme_app.tasks.update_rs_folio_field', request.user.id, task_name='update_folios_in_dam', hook='dalme_app.utils.send_message')
#
#
# def rebuild_search_index(request):
#     # async_task('dalme_app.tasks.update_search_index', request.user.id, task_name='rebuild_search_index', hook='dalme_app.utils.send_message')
#     call_command('search_index', '--rebuild', '-f')
#     return 'Process started...'


def import_languages(request):  # noqa: ARG001
    file = os.path.join('templates', 'menus', 'uk.json')
    with open(file) as fp:
        text = json.load(fp)
        for item in text:
            if not Language.objects.filter(glottolog_id=item['properties']['language']['id']).exists():
                new_lang = Language()
                new_lang.glottolog_id = item['properties']['language']['id']
                new_lang.iso6393_id = item['properties']['language']['hid']
                new_lang.name = item['properties']['language']['name']
                new_lang.type = item['properties']['language']['level']
                new_lang.save()
                if item['properties']['language']['newick']:
                    p = re.compile(r'\'([a-z0-9 ]+) \[(\w+)\]\'', re.IGNORECASE)
                    m = p.findall(item['properties']['language']['newick'])
                    if m:
                        parent_object = Language.objects.get(glottolog_id=item['properties']['language']['id'])
                        for i in m:
                            if not Language.objects.filter(glottolog_id=i[1]).exists():
                                new_dia = Language()
                                new_dia.glottolog_id = i[1]
                                new_dia.name = i[0]
                                new_dia.type = 'dialect'
                                new_dia.parent = parent_object
                                new_dia.save()
    return 'okay'


def remove_11600(request):  # noqa: ARG001
    Page.objects.filter(dam_id=11600).update(dam_id=None)
    return 'Done'


def migrate_datasets(request):  # noqa: ARG001
    owner = User.objects.get(pk=5)
    datasets = list({i.value_STR for i in Attribute.objects.filter(attribute_type=27)})
    result = 'Unique dataset names = ' + str(len(datasets)) + ' | '
    new_sets = []
    for ds in datasets:
        new_set = Set(
            set_type=4,
            endpoint='sources',
            permissions=4,
            description='Auto-generated from dataset attribute.',
            name=ds,
            owner=owner,
        )
        new_sets.append(new_set)
    Set.objects.bulk_create(new_sets)

    result = result + 'New sets created = ' + str(len(new_sets)) + ' | '
    sources = Attribute.objects.filter(attribute_type=27)
    result = result + 'Sources to add = ' + str(sources.count()) + ' | '

    new_members = []
    for s in sources:
        source_object = Source.objects.get(pk=s.object_id)
        set_object = Set.objects.get(name=s.value_STR)
        if not Set_x_content.objects.filter(set_id=set_object.id, object_id=s.object_id).exists():
            new_entry = Set_x_content(
                set_id=set_object,
                content_object=source_object,
            )
            new_members.append(new_entry)
    Set_x_content.objects.bulk_create(new_members)

    result = result + 'New members created = ' + str(len(new_members)) + ' | '
    sources.delete()
    return result + 'Attributes deleted.'


def add_to_public_register(request):  # noqa: ARG001
    public_sources = Source.objects.filter(workflow__is_public=True)
    ct = ContentType.objects.get_for_model(public_sources.first())
    for source in public_sources:
        PublicRegister.objects.create(
            object_id=source.id,
            content_type=ct,
        )
    return 'done'


def geolocate_locales(request):  # noqa: ARG001
    locales = LocaleReference.objects.all()
    geolocator = AlgoliaPlaces(domain='places-dsn.algolia.net')
    errors = {}
    for loc in locales:
        try:
            location = geolocator.geocode(f'{loc.name}, {loc.administrative_region}, {loc.country.name}')
            loc.latitude = location.latitude
            loc.longitude = location.longitude
            loc.save()
        except AttributeError:
            location = geolocator.geocode(f'{loc.name}')
            loc.latitude = location.latitude
            loc.longitude = location.longitude
            loc.save()
        except Exception as e:  # noqa: BLE001
            errors[loc.name] = e

    return errors


def test_expression(request):  # noqa: ARG001
    sources = Source.objects.filter(modification_user__isnull=True)
    for source in sources:
        source.modification_user = source.creation_user
        source.save()
    return sources.count()


def fix_users(records):
    # records = Attribute.objects.all()
    for s in records:
        c_user = User.objects.get(username=s.creation_username)
        m_user = User.objects.get(username=s.modification_username)
        s.creation_user = c_user
        s.owner = c_user
        s.modification_user = m_user
        s.save()


# REMOVE DUPLICATES
# def test_expression2(request):
#     # Authority = 128
#     # Format = 129
#     for row in Attribute.objects.filter(attribute_type__in=[128, 129]).reverse():
#         if Attribute.objects.filter(object_id=row.object_id, attribute_type=row.attribute_type).count() > 1:
#             row.delete()
#     return 'done'

# def test_expression2(request):
# worksets = Workset.objects.all()
# set_names = [i.name for i in Set.objects.all()]
# for ws in worksets:
#     if ws.name not in set_names:
#         set_para = {
#             'name': ws.name,
#             'set_type': 4,
#             'endpoint': ws.endpoint,
#             'owner': ws.owner,
#             'set_permissions': 2,
#             'description': ws.description,
#         }
#         new_set = Set(**set_para)
#         new_set.save()
#         set_object = Set.objects.get(pk=new_set.id)
#         old_qset = json.loads(ws.qset)
#         new_members = []
#         for k, v in old_qset.items():
#             if Source.objects.filter(pk=v['pk']).exists():
#                 source_object = Source.objects.get(pk=v['pk'])
#                 new_entry = Set_x_content()
#                 new_entry.set_id = set_object
#                 new_entry.content_object = source_object
#                 new_entry.workset_done = v.get('done', False)
#                 new_members.append(new_entry)
#         Set_x_content.objects.bulk_create(new_members)
# result = record.source_pages.all().select_related('transcription')
# eps = [i.transcription.entity_phrases.filter(content_type=115) for i in result]
# eps = [i.transcription.entity_phrases.filter(content_type=104) for i in record.source_pages.all().select_related('transcription')]
# result2 = eps[0].union(*eps[1:])
# return record.agents[0].relations.all()[0].target_object.std_name
# record = Page.objects.get(pk='44c79e6a8a4b4b50aa7a1b9d6bb61134')
# pol = record.sources.all()[0].source.parent.parent.attributes.get(attribute_type=144).value_STR
# pol2 = json.loads(pol)['id']
# rights_obj = RightsPolicy.objects.get(pk=pol2)
# # return model_to_dict(rights_obj, fields=['rights_status', 'notice_display', 'rights_notice'])
# ret_dict = {'status': rights_obj.get_rights_status_display(), 'display_notice': rights_obj.notice_display, 'notice': json.loads(rights_obj.rights_notice)}
# return record.get_rights()['notice']['@ita']


def replace_in_transcription(request):  # noqa: ARG001
    inventories = Source.objects.filter(
        type=13,
        short_name__contains='FF 1009',
        creation_username='pizzorno',
        modification_username='pizzorno',
    )
    for inv in inventories:
        if inv.pages:
            for fol in inv.pages.all():
                if fol.sources.first().transcription:
                    tr_id = fol.sources.first().transcription.id
                    text = fol.sources.first().transcription.transcription
                    text = text.replace(
                        "<gap reason='not transcribed' extent='unknown'/>",
                        '<metamark function="leader" rend="dashes"/>',
                    )
                    Transcription.objects.filter(pk=tr_id).update(transcription=text)
    return 'cool'


def import_transcriptions(request):  # noqa: ARG001
    data = []
    count = 0
    current_id = 'bc3a2c32639e44d6b5a21829b42ae0b5'
    for e in data:
        # Manage counter for folio order.
        if e[0] == current_id:
            count = count + 1
        else:
            count = 1
            current_id = e[0]

        # Create the transcription record.
        new_tr = Transcription()
        new_tr.transcription = e[4]
        new_tr.author = 'smail'
        new_tr.version = 0
        new_tr.save()

        # Create the page.
        source_object = Source.objects.get(pk=e[0])
        source_object.pages.create(
            name=e[1],
            dam_id=e[2],
            order=count,
            through_defaults={'transcription': new_tr},
        )
        # Create dan's done tag if necessary.
        if e[3] == 1:
            source_object.tags.create(
                tag_type='C',
                tag='Done',
                tag_group='DLS_Lucca_Transcription_Review',
            )

        # Update source's has_inventory field.
        source_object.has_inventory = 1
        source_object.save()

    return 'done'


def merge_attributes_csv():
    _file = 'attribute_date.csv'
    _file = os.path.join('dalme_app', _file)
    df = pd.read_csv(_file)
    results = []
    for i, row in df.iterrows():
        att_id = row['attribute_id_id']
        try:
            if not pd.isnull(row['value_day']) and not pd.isnull(row['value_month']):
                day = int(row['value_day'])
                month = int(row['value_month'])
                year = int(row['value_year'])
                the_date = date(year, month, day)
                date_str = the_date.strftime('%d-%b-%Y').lstrip('0').replace(' 0', ' ')
                att = Attribute.objects.get(pk=att_id)
                att.value_DATE_d = day
                att.value_DATE_m = month
                att.value_DATE_y = year
                att.value_DATE = the_date
                att.value_STR = date_str
                att.save()
                results.append(str(i) + ', ' + att_id + ': OK')

            elif not pd.isnull(row['value_month']):
                month = int(row['value_month'])
                year = int(row['value_year'])
                the_date = date(year, month, 1)
                date_str = the_date.strftime('%b-%Y')
                att = Attribute.objects.get(pk=att_id)
                att.value_DATE_m = month
                att.value_DATE_y = year
                att.value_STR = date_str
                att.save()
                results.append(str(i) + ', ' + att_id + ': OK')

            else:
                date_str = row['value_year']
                year = int(date_str)
                att = Attribute.objects.get(pk=att_id)
                att.value_DATE_y = year
                att.value_STR = date_str
                att.save()
                results.append(str(i) + ', ' + att_id + ': OK')

        except:  # noqa: E722
            results.append(str(i) + ', ' + att_id + ': BAD')

    return results
