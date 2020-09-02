import json
import os
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from async_messages import get_messages
from djangosaml2idp.processors import BaseProcessor
from typing import Dict
from dalme_app.models import Task
from django.template import defaultfilters
import re







class AsyncMiddleware(MiddlewareMixin):
    """
    Fix for django-async-messages to work with newer Django versions.
    This is the same as the original middleware class with two changes:
    It uses the MiddlewareMixin for compatibility and it calls
    request.user.is_authenticated without brackets.
    """

    def process_response(self, request, response):
        """
        Check for messages for this user and, if it exists,
        call the messages API with it
        """
        if hasattr(request, "session") and hasattr(request, "user") and request.user.is_authenticated:
            msgs = get_messages(request.user)
            if msgs:
                for msg, level in msgs:
                    messages.add_message(request, level, msg)
        return response


# BasePermission Override to implement per-ownership permission_classes
class IsOwnerOrReadOnly(permissions.BasePermission):
    """ Object-level permission to only allow owners of an object to edit it. """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        elif obj.owner == request.user or request.user.is_superuser:
            return True
        else:
            return False


# Routers to support external databases (WP, DAM, Wiki)
class ModelDatabaseRouter(object):
    """Allows each model to set its own db target"""

    def db_for_read(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def db_for_write(self, model, **hints):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            return model._meta.in_db
        return None

    def allow_syncdb(self, db, model):
        # Specify target database with field in_db in model's Meta class
        if hasattr(model._meta, 'in_db'):
            if model._meta.in_db == db:
                return True
            else:
                return False
        else:
            # Random models that don't specify a database can only go to 'default'
            if db == 'default':
                return True
            else:
                return False


# djangosaml2idp processor
class SAMLProcessor(BaseProcessor):
    """ subclasses the default djangosaml2idp processor
    to allow for special fields to be included in response """

    def create_identity(self, user, sp_attribute_mapping: Dict[str, str]) -> Dict[str, str]:
        results = {}
        for user_attr, out_attr in sp_attribute_mapping.items():
            attr_lst = user_attr.split('.')
            if len(attr_lst) > 1 and attr_lst[0] == 'profile':
                results[out_attr] = getattr(user.profile, attr_lst[1])
            if user_attr == 'groups':
                results[out_attr] = list(user.groups.values_list('name', flat=True))
            # elif user_attr == 'profile_image':
            #     results[out_attr] = user.profile.profile_image
            elif hasattr(user, user_attr):
                attr = getattr(user, user_attr)
                results[out_attr] = attr() if callable(attr) else attr
        return results


class DALMEMenus():
    ''' Class for managing menus throughout the app '''

    def __init__(self, request, state):
        self.dropdowns = self.menu_constructor(request, 'dropdown', 'dropdown_menu_default', state)
        self.sidebar = self.menu_constructor(request, 'sidebar', 'sidebar_menu_default', state)

    def menu_constructor(self, request, constructor_type, template, state):
        '''Builds menus based on an item_constructor_type and a json file describing the menu items.'''
        user_id = request.user.id
        _output = ''
        template = os.path.join('dalme_app', 'config', template + '.json')
        with open(template, 'r') as fp:
            menu = json.load(fp)
        for item in menu:
            if item.get('permissions') is None or self.check_group(request, item['permissions']):
                _output += self.sidebar_menu(_output, state, **item) if constructor_type == 'sidebar' else self.dropdown_menu(_output, state, **item)
        if constructor_type == 'dropdown_item':
            _output = self.dropdown_tasks(_output, user_id)
        return [_output]

    def sidebar_menu(self, wholeMenu, state, dropdown=None, text=None, iconClass=None, link=None, counter=None,
                     section=None, child=None, divider=None, itemClass=None, close_dropdown=None, blank=None,
                     permissions=None):
        if section:
            currentItem = '<div class="sidebar-heading">{}</div><hr class="sidebar-divider">'.format(text)
        elif divider:
            currentItem = '<hr class="sidebar-divider">'
        elif close_dropdown:
            currentItem = '</li>'
        elif dropdown:
            currentItem = '<li class="nav-item'
            if text in state['breadcrumb']:
                currentItem += ' active'
            currentItem += '">'
            currentItem += '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapse{}" aria-expanded="true" \
                            aria-controls="collapse{}">'.format(itemClass, itemClass)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a>'.format(text)
            if text in state['breadcrumb'] and state['sidebar'] != 'toggled':
                currentItem += '<div id="collapse{}" class="collapse show" aria-labelledby="heading{}" \
                                data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            else:
                currentItem += '<div id="collapse{}" class="collapse" aria-labelledby="heading{}" \
                                data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            currentItem += '<div class="bg-white py-2 collapse-inner rounded">'
        elif child:
            currentItem = '<a class="collapse-item'
            if text in state['breadcrumb']:
                currentItem += ' active'
            currentItem += '" href="{}"'.format(link)
            if blank:
                currentItem += ' target="_blank"'
            currentItem += '><i class="fas fa-fw {}"></i> {}</a>'.format(iconClass, text)
        else:
            currentItem = '<li class="nav-item'
            if text == 'Dashboard':
                currentItem += ' dash-menu'
            if text in state['breadcrumb']:
                currentItem += ' active'
            currentItem += '">'
            currentItem += '<a class="nav-link" href="{}">'.format(link)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a></li>'.format(text)
        return currentItem

    def dropdown_menu(self, wholeMenu, state, topMenu=None, infoPanel=None, title=None, itemClass=None, iconClass=None,
                      childrenIconClass=None, children=None, text=None, link=None, action=None, divider=None, section=None,
                      counter=None, circleColour=None, moreText=None, moreLink=None, permissions=None, tooltip=None):
        if link:
            currentItem = '<li class="nav-item dropdown no-arrow topbar-border-left">'
            currentItem += '<a class="nav-link dropdown-toggle" href="{}" id="{}button" role="button" data-toggle="tooltip" \
                            data-placement="bottom" title="{}" data-delay=\'&#123;"show":"1000", "hide":"0"&#125;\'>'.format(link, itemClass, tooltip)
            currentItem += '<i class="{} fa-g"></i></a>'.format(iconClass)
        else:
            currentItem = '<li class="nav-item dropdown no-arrow topbar-border-left" data-toggle="tooltip" data-placement="bottom" \
                           title="{}" data-delay=\'&#123;"show":"1000", "hide":"0"&#125;\'>'.format(tooltip)
            currentItem += '<a class="nav-link dropdown-toggle" href="#" id="{}Dropdown" role="button" data-toggle="dropdown" \
                            aria-haspopup="true" aria-expanded="false">'.format(itemClass)
            currentItem += '<i class="{} fa-g"></i>'.format(iconClass)
            currentItem += '</a><div class="dropdown-menu dropdown-menu-right animated--grow-in" \
                            aria-labelledby="{}Dropdown">'.format(itemClass)
            for child in children:
                if 'divider' in child:
                    currentItem += '<div class="dropdown-divider"></div>'
                else:
                    currentItem += '<a class="dropdown-item" href="{}"'.format(child['link'])
                    if 'action' in child:
                        currentItem += '" onclick="{}"'.format(child['action'])
                    currentItem += '>'
                    if 'iconClass' in child:
                        currentItem += '<i class="{} fa-fw mr-2 text-gray-400"></i>{}</a>'.format(child['iconClass'], child['text'])
                    else:
                        currentItem += '<i class="{} fa-fw mr-2 text-gray-400"></i>{}</a>'.format(childrenIconClass, child['text'])
            currentItem += '</div></li> '
        return currentItem

    def dropdown_tasks(self, wholeMenu, user_id):
        button = ''
        dropmenu = ''
        overdue = False
        counter = False
        if Task.objects.filter(assigned_to=user_id, completed=0).exists():
            tasks = Task.objects.filter(assigned_to=user_id, completed=0)
            counter = tasks.count()
            tasks = tasks[:5]
            for task in tasks:
                dropmenu += '<div class="dropdown-tasks-item">\
                                <div class="dropdown-tasks-text">\
                                    <a href="/tasks/{}" class="dropdown-task-title">{}</a>'.format(task.id, task.title)
                dropmenu += '<div class="dropdown-task-description">{}</div></div>'.format(task.description)
                dropmenu += '<div class="dropdown-tasks-info"><div class="dropdown-tasks-pill">{}</div>'.format(task.task_list)
                if task.due_date:
                    dropmenu += '<div class="dropdown-tasks-pill task-'
                    if task.overdue_status():
                        overdue = True
                        dropmenu += 'over'
                    dropmenu += 'due">Due: {}</div>'.format(task.due_date.strftime('%d-%b-%Y'))
                dropmenu += '</div><div class="dropdown-tasks-buttons"><div class="btn_task_complete" id="{}" onclick="task_set_state({}, {})">\
                            <i class="far fa-square fa-lg"></i></div></div></div>'.format('task_'+str(task.id), task.id, 'False')
        else:
            dropmenu += '<div class="dropdown-tasks-empty">There are currently no tasks in your queue.</div>'
        dropmenu += '<a class="dropdown-tasks-action dropdown-tasks-action-rb" href="{}">{}</a>'.format('/', 'My Tasks')
        dropmenu += '<a class="dropdown-tasks-action" href="{}">{}</a></div></li>'.format('/tasks/', 'All Tasks')

        button = '<li class="nav-item dropdown no-arrow topbar-border-left" data-toggle="tooltip" data-placement="bottom" title="Your task list" \
                  data-delay=\'{"show":"1000", "hide":"0"}\'>'
        button += '<a class="nav-link dropdown-toggle" href="#" id="tasksDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" \
                   aria-expanded="false">'
        button += '<i class="fas fa-tasks fa-fw"></i>'
        if counter:
            if overdue:
                button += '<span class="badge topbar-badge-alert">{}</span>'.format(counter)
            else:
                button += '<span class="badge topbar-badge">{}</span>'.format(counter)
        button += '</a><div class="dropdown-tasks dropdown-menu dropdown-menu-right animated--grow-in" aria-labelledby="tasksDropdown">'
        button += '<div class="dropdown-tasks-header">Your Tasks <div class="dropdown-task-add ml-auto" onclick="create_task()">Add New <i class="fa fa-plus fa-fw"></i></div></div>'
        wholeMenu += button
        wholeMenu += dropmenu
        return wholeMenu

    def check_group(self, request, group_list):
        """ Checks if the current user is a member of any of the groups in the passed list. """
        user_groups = [i.name for i in request.user.groups.all()]
        result = [i for i in user_groups if i in group_list]
        if result or request.user.is_superuser:
            return True
        else:
            return False


class DALMEDateRange:
    ''' Class for managing date ranges throughout the app '''

    months_long = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    months_short = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
    months_int = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

    def __init__(self, start_date, end_date):
        self.long = self.format_range(start_date, end_date, 'long')
        self.short = self.format_range(start_date, end_date, 'short')

    def format_range(self, start_date, end_date, format):
        if start_date == end_date:
            return self.format_date(start_date, format)
        else:
            start_date = self.get_date_elements(start_date, format)
            end_date = self.get_date_elements(end_date, format)
            if start_date[2] == end_date[2]:
                if start_date[1] == end_date[1] and start_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} to {} {}, {}' if format == 'long' else '{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), str(end_date[0]), start_date[1], start_date[2])
                    else:
                        return self.format_date(start_date, format)
                elif start_date[1] is not None and end_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} {} to {} {}, {}' if format == 'long' else '{}/{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), start_date[1], str(end_date[0]), end_date[1], start_date[2])
                    else:
                        range_string = '{} to {}, {}' if format == 'long' else '{}-{}/{}'
                        return range_string.format(start_date[1], end_date[1], start_date[2])
            else:
                if start_date[1] is not None and end_date[1] is not None:
                    if start_date[0] is not None and end_date[0] is not None:
                        range_string = '{} {}, {} to {} {}, {}' if format == 'long' else '{}/{}/{}-{}/{}/{}'
                        return range_string.format(str(start_date[0]), start_date[1], start_date[2], str(end_date[0]), end_date[1], end_date[2])
                    else:
                        range_string = '{} {} to {} {}' if format == 'long' else '{}/{}-{}/{}'
                        return range_string.format(start_date[1], start_date[2], end_date[1], end_date[2])
                else:
                    range_string = '{} to {}' if format == 'long' else '{}-{}'
                    return range_string.format(start_date[2], end_date[2])

    def get_day(self, date):
        return date[0] if len(date) == 3 else None

    def get_month(self, date, format):
        if len(date) > 1:
            if len(date[-2]) == 3:
                m_int = self.months_int[date[-2]]
            else:
                m_int = int(date[-2])
            return self.months_short[m_int] if format == 'short' else self.months_long[m_int]
        else:
            return None

    def get_year(self, date):
        return date[-1]

    def format_date(self, date, format):
        date = self.get_date_elements(date, format) if type(date) is not list else date
        if date[0] is not None:
            return '{} {}, {}'.format(str(date[0]), date[1], date[2]) if format == 'long' else '{}/{}/{}'.format(str(date[0]), date[1], date[2])
        elif date[1] is not None:
            return '{} {}'.format(date[1], date[2])
        else:
            return date[2]

    def get_date_elements(self, date, format):
        if '-' in str(date):
            date = str(date).split('-')
        else:
            date = [date]
        return [self.get_day(date), self.get_month(date, format), self.get_year(date)]


def round_timesince(d):
    chunks = {
        'minute': 60,
        'hour': 24,
        'day': 30,
        'week': 4,
        'month': 12
    }
    d_string = defaultfilters.timesince(d)
    if ',' in d_string:
        d_list = re.findall(r"[\w\d']+", d_string)
        for i, j in enumerate(d_list):
            if j[-1] == 's':
                d_list[i] = j[:-1]
        if d_list[3] in ['minute', 'hour']:
            if int(d_list[2]) / chunks[d_list[3]] >= 0.5:
                d_list[0] = int(d_list[0]) + 1
        else:
            if int(d_list[2]) / chunks[d_list[3]] >= 0.2:
                d_list[0] = int(d_list[0]) * chunks[d_list[3]] + int(d_list[2])
                d_list[1] = d_list[3]
        if int(d_list[0]) > 1:
            d_list[1] = d_list[1] + 's'
        result = str(d_list[0]) + ' ' + str(d_list[1]) + ' ago '
    else:
        if d_string == '0\xa0minutes':
            result = 'now'
        else:
            result = d_string + ' ago'
    return result
