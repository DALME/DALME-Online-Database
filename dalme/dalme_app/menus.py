from dalme_app import functions
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
import json
import os



def sidebar_menu(template='sidebar_default.json'):
    """Creates the sidebar menu based on a json file describing the menu items.
    Menus are stored in the templates directory, under the menus subdirectory.

    Menu items may have the following properties:
    text: Text to be shown in menu item.
    iconClass: Class for Font Awesome icon.
    section: If the menu item is a section marker, set this property to True.
    link: Link for menu item
    counter: Add a count of some kind to menu items. The value of this key will
        be passed to the `functions.get_count()` function, and the return value
        of that function will appear as the count.
    children: Nest additional menu items as a list under this key.

    All properties default to `None`, so if you don't want to include any
    element, just leave out that key."""

    # Get template from default location in dalme_app/templates/menus and read it
    template = os.path.join('dalme','dalme_app','templates','menus',template)
    with open(template, 'r') as fp:
        menu = json.load(fp)

    # Declare output string
    _output = ''

    # Create menu by iterating through items in json file and appending to output
    for item in menu:
        _output += sidebar_menu_item(_output,**item)

    # Return output as part of a list, because renderer expects to iterate
    return [_output]

LEVEL_LOOKUP = ['nav-second-level', 'nav-third-level', 'nav-fourth-level', 'nav-fifth-level']

def sidebar_menu_item(wholeMenu,depth=0,text=None,iconClass=None,link=None,counter=None,section=None,children=None):
    """
    Generates a menu item and incorporates it into `whoeleMenu`. This function
    calls itself to recurse through hierarchies of menus, and uses the
    `LEVEL_LOOKUP` variable with the `depth` parameter to give subheadings the
    right class.

    :param wholeMenu: The entire collection of menu items to which the current
        item will be added
    :param depth: The level of depth within the menu of the current item.
        Defaults to 0, but is incremented upon recursion
    :param text: Text of the menu item
    :param iconClass: Class for the Font Awesome icon to accompany menu item
    :param link: Link to be used as the href for the menu item
    :param counter: What kind of thing to count and add to the menu. The value
        of this parameter will be passed to the `functions.get_count()` function
        and the return value will be incorporated into the menu item
    :param section: If this parameter is set to true, the menu item will be
        given a class for a menu section header.
    :param children: List of child menu items to appear under this item. Items
        should be dictionaries, with keys corresponding to the parameters of
        this function
    """
    currentItem = '<li '
    # If this item is a section header and the whole menu is empty, this is the
    # first section header
    if section and wholeMenu == '':
        currentItem += 'class="sidebar-section-first"'
    elif section:
        currentItem += 'class="sidebar-section"'
    currentItem += '>'

    if link:
        currentItem += '<a href="{}">'.format(link)

    if iconClass:
        currentItem += '<i class="fa {} fa-fw"></i> '.format(iconClass)

    if text:
        currentItem += text

    if counter:
        counter = functions.get_count(counter)
        currentItem += '<div class="menu-counter">{}</div>'.format(counter)

    if children:
        # If this item has children, append an arrow to show that
        currentItem += '<span class="fa arrow"></span>'

    if link:
        # Close the anchor tag if it was opened
        currentItem += '</a>'

    if children:
        # If there are child items, start a new unordered list based on the
        # depth. If depth is not defined in LEVEL_LOOKUP, that <ul> doesn't get
        # a class, so it might look weird.
        try:
            currentItem += '<ul class="nav {}">'.format(LEVEL_LOOKUP[depth])
        except IndexError:
            print(depth)
            currentItem += '<ul class="nav">'
        for child in children:
            # For each child item, provide the parameters it defines to this
            # function, incrementing the depth
            currentItem += sidebar_menu_item(currentItem,depth=depth+1,**child)
        currentItem += '</ul>'
    currentItem += '</li>'

    return currentItem


def dropdowns(username):
    """ creates the top right dropdowns """
    logout = 'Logout ' + username

    dropdowns = [
        ['fa fa-gear', 'dropdown-scripts', [
                ['1', '/script/import_sources_csv', 'fa fa-gears', 'Import Sources CSV'],
                ['1', '/script/test_expression', 'fa fa-gears', 'Test Expression'],
            ]

        ],
        ['fa fa-list-alt', 'dropdown-ref', [
                ['1', '/list/errors', 'fa fa-medkit', 'Error codes'],
                ['divider'],
                ['0', '#', 'fa fa-list-alt', 'UI Reference:'],
                ['1', '/UIref/dash_demo', 'fa fa-dot-circle-o', 'Dashboard Content'],
                ['1', '/UIref/panels-wells', 'fa fa-dot-circle-o', 'Panels and Wells'],
                ['1', '/UIref/buttons', 'fa fa-dot-circle-o', 'Buttons'],
                ['1', '/UIref/notifications', 'fa fa-dot-circle-o', 'Notifications'],
                ['1', '/UIref/typography', 'fa fa-dot-circle-o', 'Typography'],
                ['1', '/UIref/icons', 'fa fa-dot-circle-o', 'Icons'],
                ['1', '/UIref/grid', 'fa fa-dot-circle-o', 'Grid'],
                ['1', '/UIref/tables', 'fa fa-dot-circle-o', 'Tables'],
                ['1', '/UIref/flot', 'fa fa-dot-circle-o', 'Flot Charts'],
                ['1', '/UIref/morris', 'fa fa-dot-circle-o', 'Morris.js Charts'],
                ['1', '/UIref/forms', 'fa fa-dot-circle-o', 'Forms'],
            ]
        ],
        ['fa fa-user', 'dropdown-user', [
                ['1', '#', 'fa fa-user', 'Profile'],
                ['1', '#', 'fa fa-gear', 'Settings'],
                ['divider'],
                ['1', '/logout/', 'fa fa-sign-out', logout],
            ]
        ],
    ]

    user_id = User.objects.get(username=username).pk
    results = []
    _output = ''

    for item in dropdowns:
        if item[0] == 'fa-tasks':
            _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '"><form action="" method="POST">'

        else:
            _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '">'

        for menu in item[2]:
            if menu[0] == 'divider':
                _output = _output + '<li class="divider"></li>'

            elif menu[0] == '0':
                _output = _output + '<li class="dropdown-section"><i class="' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</li>'

            elif menu[0] == '1':
                _output = _output + '<li><a href="' + menu[1] + '"><i class="' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</a></li>'

            elif menu[0] == '2':
                _output = _output + '<li><a href="' + menu[1] + '"><div><input class="dropdown-checkbox" type="checkbox" name="mark_done" value="' + menu[4]+ '" id="mark_done_' + menu[4] + '">' + menu[3] + '<span class="pull-right text-muted"><em>Due: ' + menu[6] + '</em></span></div><div><em>Created: ' + menu[5] + ' By: ' + menu[7] + '</em></div></a></li>'

            elif menu[0] == '3':
                _output = _output + '<li class="divider"></li><li><a class="text-center" href="' + menu[1] + '"><strong>' + menu[2] + ' </strong><i class="fa fa-angle-right"></i></a></li>'

        _output = _output + '</ul></li>'

        results.append(_output)

    return results
