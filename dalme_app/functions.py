"""
This file houses all of the miscellaneous functions used elsewhere in the project.
"""
import os
from django.db.models import Q
from dalme_app.menus import menu_constructor
import json
from random import randint
from dalme_app.models import *

# Security and permissions functions


def check_group(request, group_name):
    """ Checks if the current user is a member of the passed group. """
    if (request.user.groups.filter(name=group_name).exists() or request.user.is_superuser):
        result = True
    else:
        result = False
    return result

# General functions


def set_menus(request, context, state):
    bc = []
    for i in state['breadcrumb']:
        bc.append(i[0])
    state['breadcrumb'] = bc
    context['dropdowns'] = menu_constructor(request, 'dropdown_item', 'dropdowns_default.json', state)
    context['sidebar'] = menu_constructor(request, 'sidebar_item', 'sidebar_default.json', state)
    return context


# module-specific functions


def get_editor_folios(source):
    folios = source.pages.all().order_by('order')
    folio_count = len(folios)
    editor_folios = {'folio_count': folio_count}
    folio_list = []
    if folio_count == 1:
        folio_menu = '<div class="single_folio">Folio {} (1/1)</div>'.format(folios[0].name)
        folio_dict = {
            'name': folios[0].name,
            'id': str(folios[0].id),
            'dam_id': str(folios[0].dam_id),
            'order': str(folios[0].order)
            }
        transcription = Source_pages.objects.get(source=source.id, page=folios[0].id)
        if transcription.transcription:
            folio_dict['tr_id'] = str(transcription.transcription)
            transcription_version = transcription.transcription.version
            if transcription_version:
                folio_dict['tr_version'] = transcription_version
            else:
                folio_dict['tr_version'] = 0
        else:
            folio_dict['tr_id'] = "None"
            folio_dict['tr_version'] = 0
        folio_list.append(folio_dict)
    else:
        folio_menu = '<button class="editor-btn button-border-left" id="btn_prevFolio" value="" onclick="changeEditorFolio(this.value)" disabled><i class="fa fa-caret-left fa-fw"></i></button>'
        count = 0
        for f in folios:
            folio_dict = {
                'name': f.name,
                'id': str(f.id),
                'dam_id': str(f.dam_id),
                'order': str(f.order)
                }
            transcription = Source_pages.objects.get(source=source.id, page=f.id)
            if transcription.transcription:
                folio_dict['tr_id'] = str(transcription.transcription)
                transcription_version = transcription.transcription.version
                if transcription_version:
                    folio_dict['tr_version'] = transcription_version
                else:
                    folio_dict['tr_version'] = 0
            else:
                folio_dict['tr_id'] = "None"
                folio_dict['tr_version'] = 0
            if count == 0:
                folio_menu += '<button id="btn_selectFolio" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" \
                               aria-expanded="false">Folio {} (1/{})</button><div class="dropdown-menu" aria-labelledby="folios">'.format(f.name, folio_count)
                folio_menu += '<a class="dropdown-item current-folio" href="#" id="0" onclick="changeEditorFolio(this.id)">Folio {}</a>'.format(f.name)
            else:
                folio_menu += '<a class="dropdown-item" href="#" id="{}" onclick="changeEditorFolio(this.id)">Folio {}</a>'.format(count, f.name)
            count = count + 1
            folio_list.append(folio_dict)
        folio_menu += '</div><button class="editor-btn button-border-left" id="btn_nextFolio" value="1" onclick="changeEditorFolio(this.value)">\
                        <i class="fa fa-caret-right fa-fw"></i></button>'
    editor_folios['folio_menu'] = folio_menu
    editor_folios['folio_list'] = folio_list
    return editor_folios


def get_attribute_value(attribute):
    dt = attribute.attribute_type.data_type
    if dt == 'DATE':
        value = format_date(attribute, 'attribute')
    else:
        value = eval('attribute.value_'+dt)
    return value


def add_filter_options(values_exp, filter, mode):
    values_list = eval(values_exp)
    if mode == 'strict':
        op = []
    elif mode == 'check':
        op = [{'label': 'None', 'value': 'none'}]
    else:
        op = [{'label': 'Any', 'value': 'any'}, {'label': 'None', 'value': 'none'}, {'label': 'divider'}]
    filter['options'] = op + values_list
    return filter


def get_filter_lookups(type):
    lookup_dict = [
        {'label': 'is', 'value': 'exact', 'types': ['text', 'integer']},
        {'label': 'contains', 'value': 'contains', 'types': ['text']},
        {'label': 'starts with', 'value': 'startswith', 'types': ['text']},
        {'label': 'ends with', 'value': 'endswith', 'types': ['text']},
        {'label': 'year is', 'value': 'year', 'types': ['date', 'datetime']},
        {'label': 'month is', 'value': 'month', 'types': ['date', 'datetime']},
        {'label': 'day is', 'value': 'day', 'types': ['date', 'datetime']},
        {'label': 'date is', 'value': 'date', 'types': ['date', 'datetime']},
        {'label': 'hour is', 'value': 'hour', 'types': ['datetime']},
        {'label': 'minutes are', 'value': 'minute', 'types': ['datetime']},
        {'label': 'time is', 'value': 'time', 'types': ['datetime']},
        {'label': 'is greater than', 'value': 'gt', 'types': ['integer']},
        {'label': 'is greater than or equal to', 'value': 'gte', 'types': ['integer']},
        {'label': 'is less than', 'value': 'lt', 'types': ['integer']},
        {'label': 'is less than or equal to', 'value': 'lte', 'types': ['integer']},
        {'label': 'is in range', 'value': 'range', 'types': ['date', 'datetime', 'integer']},
        {'label': 'is in list', 'value': 'in', 'types': ['text', 'integer']},
        {'label': 'is matched by regex', 'value': 'regex', 'types': ['text', 'integer', 'date', 'datetime']},
        {'label': 'is empty', 'value': 'isnull', 'types': ['text', 'integer', 'date', 'datetime']},
    ]
    lookups = [{'label': i['label'], 'value':i['value']} for i in lookup_dict if type in i['types']]
    return lookups


def get_page_chain(breadcrumb, current=None):
    i_count = len(breadcrumb)
    title = ''
    if current and current != breadcrumb[i_count-1][0]:
        if len(current) > 55:
            current = current[:55] + ' <i class="fa fa-plus-circle fa-fw" data-toggle="tooltip" data-placement="bottom" title="{}"></i> '.format(current)
        for i in breadcrumb:
            if i[1] != '':
                title += '<a href="{}" class="title_link">{}</a>'.format(i[1], i[0])
            else:
                title += i[0]
            title += ' <i class="fa fa-caret-right fa-fw"></i> '
        title += '<span class="title_current">{}</span>'.format(current)
    else:
        c = 0
        while c <= i_count - 1:
            if c == i_count - 1:
                title += '<span class="title_current">{}</span>'.format(breadcrumb[c][0])
            else:
                title += breadcrumb[c][0] + ' <i class="fa fa-caret-right fa-fw"></i> '
            c = c + 1
    return title


def get_full_collection_string(t1, t2, t3, user, name):
    full_name = ''
    if name != 'My Collection':
        if t1:
            full_name += t1 + ' ≫ '
        if t2:
            full_name += t2 + ' ≫ '
        if t3:
            full_name += t3 + ' ≫ '
        full_name += name
    else:
        full_name = 'My Collection (' + user + ')'
    return full_name


def get_dam_preview(resource):
    """
    Returns the url for an image from the ResourceSpace Digital Asset Management
    system for the given resource.
    """
    endpoint = 'https://dam.dalme.org/api/?'
    user = 'api_bot'
    key = os.environ['DAM_API_KEY']
    queryParams = {
        "function": "search_get_previews",
        "param1": '!list'+str(resource),
        "param2": "",
        "param3": "",
        "param4": "0",
        "param5": "1",
        "param6": "asc",
        "param7": "",
        "param8": "scr",
        "param9": "jpg",
    }
    response = rs_api_query(endpoint, user, key, **queryParams)
    data = json.loads(response.text)
    preview_url = data[0]['url_scr']
    return preview_url


def get_unique_username(username, app):
    if app == 'wp' and wp_users.objects.filter(user_login=username).exists():
        exists = wp_users.objects.get(user_login=username)
    elif app == 'wiki' and wiki_user.objects.filter(user_name=bytes(username, encoding='ascii')).exists():
        exists = wiki_user.objects.get(user_name=bytes(username, encoding='ascii'))
    elif app == 'dam' and rs_user.objects.filter(username=username).exists():
        exists = rs_user.objects.get(username=username)
    else:
        exists = False
    if exists:
        username = username + str(randint(100, 999))
    return username


def get_counters(list):
    counters = {}
    for i in list:
        counters[i+'_count'] = get_count(i)
    return counters


def get_count(item):
    """
    Gets counts of different types of content based on `item` input string.
    Valid values are: "inventories", "objects", "wiki-articles", "assets", "notarial_sources", "sources", "biblio_sources", "archives".
    All other values for `item` return None
    """
    if item == 'inventories':
        return Source.objects.filter(is_inventory=True).count()
    elif item == 'archives':
        return Source.objects.filter(type=19).count()
    elif item == 'sources':
        return Source.objects.count()
    elif item == 'notarial_sources':
        return Source.objects.filter(Q(type=12) | Q(type=13)).count()
    elif item == 'biblio_sources':
        return Source.objects.filter(type__lte=11).count()
    elif item == 'wiki_articles':
        return wiki_page.objects.filter(page_is_new=1).count()
    elif item == 'dam_assets':
        return rs_resource.objects.count()
    else:
        return None

# formatting functions
def format_date(value, type):
    if value is not None:
        if type == 'timestamp':
            date_str = value.strftime('%d-%b-%Y@%H:%M')
        elif type == 'attribute':
            if value.value_DATE_d is None or value.value_DATE_m is None or value.value_DATE_y is None:
                date_str = value.value_STR
            else:
                date_str = value.value_DATE.strftime('%A, %d %B, %Y').lstrip("0").replace(" 0", " ")
        elif type == 'timestamp-long':
            date_str = value.strftime('%A, %d %B, %Y @ %H:%M').lstrip("0").replace(" 0", " ")
        else:
            date_str = str(value)
    else:
        date_str = None
    return date_str


def format_boolean(value):
    if value:
        return '<i class="fa fa-check-circle dt_checkbox_true"></i>'
    else:
        return '<i class="fa fa-times-circle dt_checkbox_false"></i>'


def format_user(ref, type, output=None):
    if type == 'dam':
        if Profile.objects.filter(dam_user=ref).exists():
            user = Profile.objects.get(dam_user=ref)
            if output == 'html':
                f_user = '<a href="/users/{}">{}</a>'.format(user.user.username, user.full_name)
            else:
                f_user = str(user.user.username)
        elif rs_user.objects.filter(ref=ref).exists():
            user = rs_user.objects.get(ref=ref).username
            f_user = str(user)
        else:
            f_user = 'User: ' + str(ref)
    elif type == 'username':
        user = Profile.objects.get(user__username=ref)
        if output == 'html':
            f_user = '<a href="/users/{}">{}</a>'.format(user.user.username, user.full_name)
        else:
            f_user = str(user.user.username)
    return f_user


def format_email(email):
    return '<a href="mailto:'+email+'">'+email+'</a>'


def format_rct(user, timestamp):
    f_timestamp = format_date(timestamp, 'timestamp')
    f_user = format_user(user, 'username', 'html')
    record = f_timestamp+' by '+f_user
    return record
