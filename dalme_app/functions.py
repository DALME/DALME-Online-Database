"""
This file houses all of the miscellaneous functions used elsewhere in the project.
"""
import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import connections
from dalme_app.menus import menu_constructor
from urllib.parse import urlencode
import re, json, requests, hashlib, os, uuid, calendar, datetime
import pandas as pd
import lxml.etree as etree
from random import randint
from django.db.models.query import QuerySet

from dalme_app import menus
from dalme_app.models import *
from functools import wraps

import logging
logger = logging.getLogger(__name__)

try:
    from dalme_app.scripts.db import wp_db, wiki_db, dam_db
except:
    logger.debug("Can't connect to MySQL instance containing Wiki, DAM, and WP databases.")


#Security and permissions functions
def check_group(request, group_name):
    """
    Checks if the current user is a member of the passed group.
    """
    try:
        if request.user.is_superuser:
        #if request.user.groups.filter(name=group_name).exists() or request.user.is_superuser:
            result = True
        else:
            result = False
    except:
        result = False

    return result

def in_group(group_name):
    """
    Takes a group name and checks whether the current user is in the group.
    Used by adding as decorator before function/class: @functions.in_group('group_name')
    """
    def _in_group(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            #print request.user
            if request.user.is_anonymous:
                return redirect('/admin/')
            if (not (request.user.groups.filter(name=group_name).exists())
                or request.user.is_superuser):
                raise Http404
            return view_func(request, *args, **kwargs)
        return wrapper
    return _in_group

#General functions
def set_menus(request, context, state):
    bc = []
    for i in state['breadcrumb']:
        bc.append(i[0])
    state['breadcrumb'] = bc
    context['dropdowns'] = menu_constructor(request, 'dropdown_item', 'dropdowns_default.json', state)
    context['sidebar'] = menu_constructor(request, 'sidebar_item', 'sidebar_default.json', state)
    return context

def notification(request, **kwargs):
    if 'level' and 'text' in kwargs:
        msg_level = eval('messages.'+kwargs['level'])
        msg_output = kwargs['text']
    elif 'code' in kwargs:
        base_message = Notification.objects.get(code=code)
        msg_text = base_message.text
        msg_level = base_message.level

        if 'para' in kwargs:
            para = kwargs['para']
            msg_output = msg_text.format(**para)
        elif 'data' in kwargs:
            data = kwargs['data']
            msg_output = msg_text + '<p>' + str(data) + '</p>'
        else:
            msg_output = msg_text
    else:
        msg_level = 'DEBUG'
        msg_output = 'There was a problem processing this notification: No notification code was supplied.'

    if 'user' in kwargs:
        user = kwargs['user']
        the_user = User.objects.get(username=user)
        message_user(the_user, msg_output, msg_level)

    else:
        messages.add_message(request, msg_level, msg_output)

#module-specific functions
def get_editor_folios(source):
    folios = source.pages.all().order_by('order')
    folio_count = len(folios)
    editor_folios = { 'folio_count': folio_count }
    folio_list = []
    if folio_count == 1:
        folio_menu = '<div class="single_folio">Folio {} (1/1)</div>'.format(folios[0].name)
        folio_dict = {
            'name': folios[0].name,
            'id': str(folios[0].id),
            'dam_id': str(folios[0].dam_id),
            'order': str(folios[0].order)
            }
        transcription = Source_pages.objects.get(source_id=source.id, page_id=folios[0].id)
        if transcription.transcription_id:
            folio_dict['tr_id'] = str(transcription.transcription_id)
            transcription_version = transcription.transcription_id.version
            if transcription_version:
                folio_dict['tr_version'] = transcription_version
            else:
                folio_dict['tr_version'] = 0
        else:
            folio_dict['tr_id'] = "None"
            folio_dict['tr_version'] = 0
        folio_list.append(folio_dict)
    else:
        folio_menu = '<div class="disabled-btn-left"><i class="fa fa-caret-left fa-fw"></i></div>'
        count = 1
        for f in folios:
            folio_dict = {
                'name': f.name,
                'id': str(f.id),
                'dam_id': str(f.dam_id),
                'order': str(f.order)
                }
            transcription = Source_pages.objects.get(source_id=source.id, page_id=f.id)
            if transcription.transcription_id:
                folio_dict['tr_id'] = str(transcription.transcription_id)
                transcription_version = transcription.transcription_id.version
                if transcription_version:
                    folio_dict['tr_version'] = transcription_version
                else:
                    folio_dict['tr_version'] = 0
            else:
                folio_dict['tr_id'] = "None"
                folio_dict['tr_version'] = 0
            if count == 1:
                folio_menu += '<button id="folios" type="button" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Folio {} (1/{})</button><div class="dropdown-menu" aria-labelledby="folios">'.format(f.name,folio_count)
                folio_menu += '<div class="current-folio-menu">Folio {}</div>'.format(f.name)
            elif count == 2:
                next = f.name
                folio_menu += '<a class="dropdown-item" href="#" id="{}" onclick="folioSwitch(this.id)">Folio {}</a>'.format(f.name, f.name)
            else:
                folio_menu += '<a class="dropdown-item" href="#" id="{}" onclick="folioSwitch(this.id)">Folio {}</a>'.format(f.name, f.name)
            count = count + 1
            folio_list.append(folio_dict)

        folio_menu += '</div><button type="button" class="editor-btn button-border-left" id="{}" onclick="folioSwitch(this.id)"><i class="fa fa-caret-right fa-fw"></i></button>'.format(next)

    editor_folios['folio_menu'] = folio_menu
    editor_folios['folio_list'] = folio_list

    return editor_folios

def render_transcription(transcription):
    try:
        dom = etree.fromstring(transcription)
        xslt = etree.parse(os.path.join(settings.BASE_DIR, 'dalme_app/templates/xslt/tei_transcription.xslt'))
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        render = etree.tostring(newdom)
    except:
        render = '<b>Rendering failed.</b>'
    return render

def get_attribute_value(attribute):
    dt = attribute.attribute_type.data_type
    if dt == 'DATE':
        value = format_date(attribute, 'attribute')
    else:
        value = eval('attribute.value_'+dt)
    return value

def add_filter_options(values, filter, mode='complete'):
    if mode == 'strict':
        op = []
    elif mode == 'check':
        op = [{'label':'None'}]
    else:
        op = [{'label':'Any'}, {'label':'None'}, {'label':'divider'}]

    for d in values:
        v = list(d.values())[0]
        if v != '':
            op.append({'label':v})
    filter['options'] = op
    return filter

def get_page_chain(breadcrumb, current=None):
    i_count = len(breadcrumb)
    title = ''
    if current and current != breadcrumb[i_count-1][0]:
        if len(current) > 55:
            current = current[:55] + ' <i class="fa fa-plus-circle fa-fw" data-toggle="tooltip" data-placement="bottom" title="{}"></i> '.format(current)
        for i in breadcrumb:
            if i[1] != '':
                title += '<a href="{}" class="title_link">{}</a>'.format(i[1],i[0])
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

def get_dte_options(options, field_type, *args, **kwargs):
    if field_type == 'chosen':
        opts = [{'label': "", 'value': ""}]
    else:
        opts = []
    options = eval(options)
    if type(options) is dict:
        opts.append(options)
    elif type(options) is list:
        q = eval(options[0])
        if isinstance(q, QuerySet):
            for e in q:
                opt = { 'label': getattr(e, options[1]), 'value': getattr(e, options[2]) }
                opts.append(opt)
        elif isinstance(q, tuple):
            for value, label in q:
                opt = { 'label': label, 'value': value }
                opts.append(opt)
    return opts

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
    try:
        response = rs_api_query(endpoint, user, key, **queryParams)
        data = json.loads(response.text)
        preview_url = data[0]['url_scr']
    except:
        preview_url = None

    return preview_url

def get_unique_username(username, app):
    try:
        if app == 'wp':
            exists = wp_users.objects.get(user_login=username)
        if app == 'wiki':
            exists = wiki_user.objects.get(user_name=bytes(username, encoding='ascii'))
        if app == 'dam':
            exists = rs_user.objects.get(username=username)
    except:
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

#formatting functions

def format_date(value, type):
    if type == 'timestamp':
        try:
            date_str = value.strftime('%d-%b-%Y@%H:%M')
        except:
            date_str = str(value)
    elif type == 'attribute':
        if value.value_DATE_d == None or value.value_DATE_m == None or value.value_DATE_y == None:
            date_str = value.value_STR
        else:
            date_str = value.value_DATE.strftime('%A, %d %B, %Y').lstrip("0").replace(" 0", " ")
    elif type == 'timestamp-long':
        try:
            date_str = value.strftime('%A, %d %B, %Y @ %H:%M').lstrip("0").replace(" 0", " ")
        except:
            date_str = str(value)
    else:
        date_str = str(value)
    return date_str

def format_boolean(value):
    if value:
        return '<i class="fa fa-check-circle dt_checkbox_true"></i>'
    else:
        return '<i class="fa fa-times-circle dt_checkbox_false"></i>'

def format_user(ref, type, output):
    if type == 'dam':
        if Profile.objects.get(dam_user=ref):
            user = Profile.objects.get(dam_user=ref)
            if output == 'html':
                f_user = '<a href="/users/{}">{}</a>'.format(user.user.username, user.full_name)
            else:
                f_user = str(user.user.username)
        else:
            user = rs_user.objects.get(ref=ref).username
            f_user = str(user)
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
