import os

import pandas as pd
import regex as re
from django_currentuser.middleware import _set_current_user

from django.contrib.auth.models import User

from dalme_app.models import *  # noqa

######################################
# to avoid timeouts, disable the syncing
# with ElasticSearch in devSettings:
#
# ELASTICSEARCH_DSL_AUTOSYNC = False
# ELASTICSEARCH_DSL_AUTO_REFRESH = False
#
# REMEMBER to re-enable it and to
# manually update the search index
# afterwards!
######################################


# regex substitutions to add TEI tags
re_subs_1 = [
    (r'\[(.*?)\]', r'<supplied>\1</supplied>'),
    (r'\^(.*?)\^', r'<hi rend="superscript">\1</hi>'),
    (r'-(.*?)-', r'<del rend="overstrike">\1</del>'),
    (r'\?(.*?)\?', r'<unclear>\1</unclear>'),
    (r'\<([0-9-]+|several) ([a-z]+) (.*?)\>', r'<gap extent="\1 \2" reason="\3"></gap>'),
]

re_subs_2 = [
    (r'<signe de renvoi>(.*?)<end signe de renvoi>', r'<ref target="+"></ref><note type="renvoi" xml:id="+">\1</note>'),
    # (r'\<(.*?)\>', r'<quote resp="DLS">\1</quote>')
]

italy = CountryReference.objects.get(id=143) # noqa
record_type = Content_type.objects.get(id=13) # noqa
dls = User.objects.get(id=5)
ghp = User.objects.get(id=1)

_set_current_user(ghp)


def run_commands():
    # define general variables
    # target_set = Set.objects.get(pk='bad41158-9f01-4ac2-8bc6-8d71e096dbd9') # DEVELOP
    target_set = Set.objects.get(pk='1c8a6c02-886a-4863-9b22-6c610a44d120') # noqa PRODUCTION

    # delete old Lucca records
    print(delete_old_records())

    # create new attribute types
    attribute_types = [{
            'name': 'Legal persona',
            'short_name': 'legal_persona',
            'description': 'Role played by an agent in a particular legal process.',
            'data_type': 'STR',
            'creation_user': ghp,
            'modification_user': ghp,
        },
        {
            'name': 'Social status',
            'short_name': 'social_status',
            'description': "Title, profession, or other descriptor indicating an agent's social status.",
            'data_type': 'STR',
            'creation_user': ghp,
            'modification_user': ghp,
        },
        {
            'name': 'Religion',
            'short_name': 'religion',
            'description': 'An agents stated religious affiliation.',
            'data_type': 'STR',
            'creation_user': ghp,
            'modification_user': ghp,
        },
        {
            'name': 'Sex',
            'short_name': 'sex',
            'description': 'An agents sex.',
            'data_type': 'STR',
            'creation_user': ghp,
            'modification_user': ghp,
        }]

    for at in attribute_types:
        Attribute_type.objects.get_or_create(**at) # noqa

    # fix debt value attribute: it should be decimal
    debt_value = Attribute_type.objects.get(short_name='debt_amount') # noqa
    debt_value.data_type = 'DEC'
    debt_value.save()

    # convert the FMP dataset and prepare for import
    records, locales, record_count, locale_count = convert_datasets()
    print(f'FMP dataset conversion complete. {record_count} records and {locale_count} locales generated.')

    # create locale records + create concordance placename: new ID
    locale_concordance = {'Lucca': 530}
    for placename, locale in locales.items():
        # remove empty values
        for k, v in locale.items():
            if v is None:
                del locale[k]

        # create new locale
        latitude = locale.pop('latitude', None)
        longitude = locale.pop('longitude', None)
        defaults = {'latitude': latitude, 'longitude': longitude} if latitude and longitude else None
        if defaults:
            new_locale, created = LocaleReference.objects.get_or_create(**locale, defaults=defaults) # noqa
        else:
            new_locale, created = LocaleReference.objects.get_or_create(**locale) # noqa
        # add entry to concodance
        locale_concordance[placename] = new_locale.id

    # process records
    count = 0
    for record in records:
        attributes = record.pop('attributes', None)
        comments = record.pop('comments', None)
        pages = record.pop('pages', None)
        named_persons = record.pop('named_persons', None)
        locale_name = None
        locale_object = None

        # create source
        source = Source.objects.create(**record) # noqa

        # create workflow
        Workflow.objects.create( # noqa
            source=source,
            last_modified=source.modification_timestamp,
            last_user=ghp,
        )

        # add attributes
        for short_name, values in attributes.items():
            # IGNORE None values
            if type(values) is dict:
                v_check = False
                for k, v in values.items():
                    if v is not None:
                        v_check = True
            else:
                v_check = values is not None

            if v_check:
                # LOCALE requires special treatment as it needs to refer to new ID via concordance created earlier
                if short_name == 'locale':
                    locale_id = locale_concordance[values]
                    locale_name = values
                    locale_object = LocaleReference.objects.get(id=locale_id) # noqa
                    values = {'value_JSON': {'id': locale_id, 'class': 'LocaleReference'}}

                attribute_type = Attribute_type.objects.get(short_name=short_name) # noqa
                values['attribute_type'] = attribute_type
                source.attributes.create(**values)

        # add to set
        Set_x_content.objects.create(set_id=target_set, content_object=source) # noqa

        # create comments if any
        if comments:
            comments = comments.replace('\\n', '\n')
            source.comments.create(
                body=comments,
                creation_user=dls,
                modification_user=dls,
            )

        # create pages
        transcription_records = []
        if pages:
            for page in pages:
                text = page.pop('transcription', None)
                new_page = source.pages.create(**page)

                # create transcriptions
                if text:
                    transcription = Transcription.objects.create(transcription=text, author='smail') # noqa
                    transcription_records.append(transcription)
                    sp = new_page.sources.first()
                    sp.transcription = transcription
                    sp.save()

        # process named_persons
        if named_persons:
            tr_block = '<ab type="context">\n'

            for person in named_persons:
                name_phrase = person.pop('name_phrase', None)
                residence_phrase = person.pop('residence_phrase', None)
                legal_persona = person.pop('legal_persona', None)
                person_attributes = {key: value for key, value in person.items() if value is not None}

                if legal_persona and name_phrase:
                    agent, created = Agent.objects.get_or_create(standard_name=name_phrase[:254], type=1) # noqa
                    entity_phrase = agent.instances.create(transcription_id=transcription)

                    attribute_lp = Attribute_type.objects.get(short_name='legal_persona') # noqa
                    entity_phrase.attributes.create(**{'attribute_type': attribute_lp, 'value_STR': legal_persona})

                    if person_attributes:
                        for short_name, value in person_attributes.items():
                            attribute_type = Attribute_type.objects.get(short_name=short_name) # noqa
                            agent.attributes.update_or_create(**{'attribute_type': attribute_type, 'value_STR': value})

                    tr_block += f'{legal_persona}: <rs type="agent" subtype="person" key="{entity_phrase.id}">{name_phrase}</rs>'

                if residence_phrase:
                    if residence_phrase == locale_name:
                        place, created = Place.objects.get_or_create(standard_name=residence_phrase[:254], locale=locale_object) # noqa
                        entity_phrase = place.instances.create(transcription_id=transcription)

                        tr_block += f' <rs type="place" key="{entity_phrase.id}">{residence_phrase}</rs>\n'

                    else:
                        tr_block += f' <rs type="place">{residence_phrase}</rs>\n'
                else:
                    tr_block += '\n'

            tr_block += '</ab>\n'

            for t in transcription_records:
                t.transcription = tr_block + t.transcription
                transcription.save()

        count += 1
        if count % 10 == 0:
            print(f'{count} records processed.')

    return 'Done.'


def delete_old_records():
    records = Source.objects.filter(type=13, name__icontains='di lucca') # noqa
    print(f'Deleting {records.count()} records...')
    records.delete()
    return 'Records deleted.'


def convert_datasets():
    # load datasets
    root = os.path.dirname(os.path.abspath(__file__))
    acts = pd.read_csv(os.path.join(root, 'data', 'Lucca_act_metadata.csv'), header=0, index_col=None)
    folios = pd.read_csv(os.path.join(root, 'data', 'Lucca_folios.csv'), header=0, index_col=None)
    names = pd.read_csv(os.path.join(root, 'data', 'Lucca_names_unstandardised.csv'), header=0, index_col=None)
    value_data = pd.read_csv(os.path.join(root, 'data', 'Lucca_value_data.csv'), header=0, index_col=None)

    # register/file unit IDs in online database
    register_conc = {
        116: '78a52237-3bd0-47bf-a071-9c3f76243bdb',
        33: '05c64292-62d1-4333-a259-df078155bc8a',
        44: '2654f25b-31a8-47df-8e3f-2bf9c6db1d71',
        50: 'b83a5e55-1874-4bbb-9a57-440c088f8251',
        57: '4487e376-0a86-4f2c-bff1-23bd5870a998',
        80: '908785de-a5d7-4bab-b90b-3a95d40782c2',
        83: 'e38ac286-95e8-49d5-8a69-a219fb2856db',
    }

    # acts to ignore
    ignore = [round(row['act_id']) for i, row in folios[folios['notes_eric'].eq('[delete act]')].iterrows()]
    ignore += [1126, 1127, 1128, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 2732, 2733, 2734, 3437, 3438]

    # acts that need to be reordered
    reorder = {
        456: 457,
        457: 456,
        849: 850,
        850: 851,
        851: 849,
    }

    # lists to hold new db records
    records = []
    locales = {}

    # for index, row in acts.head(10).iterrows():
    for _index, row in acts.iterrows():
        act_id = row['Act ID']
        if act_id not in ignore:
            if act_id <= 2024:
                ref_id = reorder[act_id] if act_id in reorder else act_id
            elif act_id >= 2025 and act_id <= 2464:
                ref_id = act_id + 1
            else:
                ref_id = act_id + 2

            record = {
                'name': f'Act {ref_id}, Podestà di Lucca {round(row["subsource_number"])}, {row["Act Folio_Page"]}',
                'short_name': f'Act {ref_id}, PdL {round(row["subsource_number"])}',
                'type': record_type,
                'parent': Source.objects.get(pk=register_conc[row["subsource_number"]]), # noqa
                'has_inventory': True,
                'comments': get_value(row['Unified Comments']),
                'owner': dls,
            }

            attributes = {
                'mk1_identifier': {'value_INT': act_id},
                'language': {'value_JSON': {'id': 618, 'class': 'LanguageReference'}},
                'record_type': {'value_STR': get_value(row['Modern Act Type Classification'])},
                'debt_unit_type': {'value_STR': get_value(row['Debt Unit Type'])},
            }

            attributes = add_dates(attributes, row)

            if pd.notna(row['Storage Start Residence']):
                placename = row['Storage Start Residence'].strip() if row['Storage Start Residence'] else None
                if placename not in locales:
                    locales[placename] = {
                        'name': placename,
                        'administrative_region': 'Tuscany',
                        'country': italy,
                        'latitude': get_value(row['Storage Start Latitude'], round_v=None),
                        'longitude': get_value(row['Storage Start Longitude'], round_v=None),
                    }
                attributes['locale'] = placename
            else:
                attributes['locale'] = 'Lucca'

            debt_data = value_data[value_data['Act Serial Number'].eq(act_id)]
            if not debt_data.empty:
                debt_data = debt_data.iloc[0]
                debt_amount = get_value(debt_data['zDEPRC Debt Amount'], round_v=2)
                if debt_amount and not debt_amount.isdigit():
                    if '.' in debt_amount:
                        tokens = debt_amount.split('.')
                        if not tokens[0].isdigit() or not tokens[1].isdigit():
                            debt_amount = None
                    else:
                        debt_amount = None

                attributes.update({
                    'debt_phrase': {'value_STR': get_value(debt_data['Original Debt Transcription'])},
                    'debt_amount': {'value_DEC': debt_amount},
                    'debt_unit': {'value_STR': get_value(debt_data['zDEPRC Debt Unit'])},
                    'debt_source': {'value_STR': get_value(debt_data['Source of Debt'])},
                })

            record['attributes'] = attributes

            res_flag = get_value(row['use_debtor_residence'])
            people = names[names['Act Serial Number'].eq(act_id)]
            if not people.empty:
                named_persons = []
                for i, person in people.iterrows():
                    if get_value(person['Full Name']) is not None:
                        named_persons.append({
                            'name_phrase': get_value(person['Full Name']),
                            'residence_phrase': get_value(person['Residence Original Transcription']),
                            'legal_persona': get_value(person['Legal Persona in Act']),
                            'social_status': get_value(person['Profession_Status']),
                            'religion': get_value(person['Religion']),
                            'sex': get_value(person['Sex']),
                        })

                record['named_persons'] = process_names(named_persons, res_flag)

            page_data = folios[folios['act_id'].eq(act_id)]
            if not page_data.empty:
                pages = []

                for i, page in page_data.iterrows():
                    i_flag = get_value(page['para_br_and'])
                    e_flag = get_value(page['para_br_item'])
                    n_flag = get_value(page['para_br_none'])
                    notes = get_value(page['notes_eric'])

                    transcription = get_value(page['transcription'])
                    if transcription and transcription != '\n':
                        clean_transcription = process_transcription(transcription, i_flag, e_flag, n_flag, notes)
                    else:
                        clean_transcription = None

                    pages.append({
                        'name': page['folio'],
                        'dam_id': get_value(page['DAM_id']),
                        'order': i + 1,
                        'transcription': clean_transcription,
                    })

                record['pages'] = pages

            records.append(record)

    return records, locales, len(records), len(locales)


def add_dates(attributes, row):
    start_date_d = get_value(row['Process Start Day'])
    start_date_m = get_value(row['Process Start Month'])
    start_date_y = get_value(row['Process Start Year'])
    end_date_d = get_value(row['Process End Day'])
    end_date_m = get_value(row['Process End Month'])
    end_date_y = get_value(row['Process End Year'])

    if start_date_d == end_date_d and start_date_m == end_date_m and start_date_y == end_date_y:
        attributes['date'] = {
            'value_DATE_d': start_date_d,
            'value_DATE_m': start_date_m,
            'value_DATE_y': start_date_y,
        }
    else:
        attributes.update({
            'start_date': {
                'value_DATE_d': start_date_d,
                'value_DATE_m': start_date_m,
                'value_DATE_y': start_date_y,
            },
            'end_date': {
                'value_DATE_d': end_date_d,
                'value_DATE_m': end_date_m,
                'value_DATE_y': end_date_y,
            },
        })

    return attributes


def get_value(v, round_v=0):
    value = v if pd.notna(v) else None
    if round_v is not None:
        if round_v == 0:
            return round(value) if type(value) is float else value
        else:
            return round(value, round_v) if type(value) is float else value
    else:
        return value


def process_transcription(data, item_flag, et_flag, none_flag, notes):
    # substitute placeholders
    if item_flag:
        data = data.replace('$', 'item')

    if et_flag:
        data = data.replace('$', 'et')

    if none_flag:
        data = data.replace('$', ',')

    # substitute context
    data = data.replace('<context>', '<gap reason="context"/>')

    # do columns
    if notes and 'columns' in notes:
        col_count = 2 if 'two columns' in notes else 3
        data = data.replace('<column 1>', f'<layout columns="{col_count}"></layout>/n<ab type="column" n="1">')
        data = data.replace('<column 2>', '</ab>/n<ab type="column" n="2">')
        if col_count == 3:
            data = data.replace('<column 3>', '</ab>/n<ab type="column" n="3">')
        data = data + '</ab></layout>'

    # add TEI tags
    for sub in re_subs_1 + re_subs_2:
        data = re.sub(sub[0], sub[1], data)

    # fix newlines
    data = data.replace('\\n', '\n')

    return data


def process_names(data, residence_flag):
    # creditor, nuncius, debtor, bailee/consul, bailee/creditor, bailee/other, purchaser, upstreamdebtor, proxydebtor, bailee/upstreamdebtor, other

    # build a table of contents for people
    tc = {}
    for i, person in enumerate(data):
        lp = person['legal_persona']
        if lp not in tc:
            tc[lp] = [i]
        else:
            tc[lp].append(i)

    # for debtor -> replace @ in phrase with text in debtor-residence field
    # instead we use TEI tags to add both to a common phrase that gets prepended to the transcription?
    debtors = tc.get('debtor', [])
    for debtor in debtors:
        person = data[debtor]
        if '@' in person['name_phrase']:
            person['name_phrase'] = person['name_phrase'].replace('@', person['residence_phrase'])

    # if residence_flag -> append debtor-residence text of debtor to bailee/consul phrase
    # INSTEAD: we copy the debtor residence to the bailee/consul residence
    if residence_flag:
        debtor = tc.get('debtor', [])[0]
        debtor_residence = data[debtor]['residence_phrase']
        if debtor_residence is not None:
            targets = tc.get('bailee/consul', [])
            for t in targets:
                data[t]['residence_phrase'] = debtor_residence

    # in the bailee/consul field -> replace "cdc" with "consuli dicti comunis"
    targets = tc.get('bailee/consul', [])
    for t in targets:
        data[t]['name_phrase'] = data[t]['name_phrase'].replace('cdc', 'consuli dicti comunis')

    # in all "bailee/creditor" fields -> delete text between square brackets
    targets = tc.get('bailee/creditor', [])
    for t in targets:
        data[t]['name_phrase'] = re.sub(r'\[.*?\]', '', data[t]['name_phrase'])

    # general clean-up, i.e. strip/trim, double spaces, etc.
    # add TEI tags
    for person in data:
        person['name_phrase'] = person['name_phrase'].replace('@', '')
        person['name_phrase'] = re.sub(r'\s+', ' ', person['name_phrase'])
        person['name_phrase'] = person['name_phrase'].strip()
        person['name_phrase'] = person['name_phrase'].replace('?fam?', 'quondam')
        person['name_phrase'] = person['name_phrase'].replace('Lucani cive', 'Lucano cive')
        person['name_phrase'] = person['name_phrase'].replace('cive Lucani', 'cive Lucano')

        for sub in re_subs_1:
            person['name_phrase'] = re.sub(sub[0], sub[1], person['name_phrase'])

        if person['residence_phrase']:
            person['residence_phrase'] = re.sub(r'\s+', ' ', person['residence_phrase'])
            person['residence_phrase'] = person['residence_phrase'].strip()

            for sub in re_subs_1:
                person['residence_phrase'] = re.sub(sub[0], sub[1], person['residence_phrase'])

    return data
