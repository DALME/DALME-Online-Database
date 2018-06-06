"""
This menus module provides a streamlined way to create menus from simple json files.
"""

from django.contrib.auth.models import User
from django.urls import reverse

import json, os

from . import functions

LEVEL_LOOKUP = ['nav-second-level', 'nav-third-level', 'nav-fourth-level', 'nav-fifth-level']

def sidebar_item(request,wholeMenu,depth=0,text=None,iconClass=None,link=None,counter=None,section=None,children=None):
    """
    Generates a menu item and incorporates it into `wholeMenu`. This function
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
            currentItem += sidebar_item(request,currentItem,depth=depth+1,**child)
        currentItem += '</ul>'
    currentItem += '</li>'

    return currentItem

def tile_item(request,wholeMenu,colourClass=None,iconClass=None,counter=None,counterTitle=None,linkTarget=None,linkTitle=None):
    currentItem = '<div class="col-lg-3 col-md-6">'

    if colourClass:
        currentItem += '<div class="panel {}">'.format(colourClass)

    currentItem += '<div class="panel-heading"><div class="row"><div class="col-xs-3">'

    if iconClass:
        currentItem += '<i class="fa {} fa-5x"></i> '.format(iconClass)

    currentItem += '</div><div class="col-xs-9 text-right">'

    if counter:
        counter = functions.get_count(counter)
        currentItem += '<div class="huge">{}</div>'.format(counter)

    if counterTitle:
        currentItem += '<div>{}</div>'.format(counterTitle)

    currentItem += '</div></div></div>'

    if linkTarget:
        currentItem += '<a href="{}" target="_blank"><div class="panel-footer">'.format(linkTarget)

    if linkTitle:
        currentItem += '<span class="pull-left">{}</span>'.format(linkTitle)

    currentItem += '<span class="pull-right"><i class="fa fa-arrow-circle-right"></i></span><div class="clearfix"></div></div></a></div></div>'

    return currentItem

def dropdown_item(request,wholeMenu,topMenu=None,title=None,itemClass=None,iconClass=None,childrenIconClass=None,children=None,text=None,link=None,divider=None,section=None,logoutMenu=None):
    """ creates items for the top right dropdowns """
    #generate dynamic menu items
    if logoutMenu:
        text = request.user.username

    #start this dropdown
    currentItem = ''
    #check if it is a top menu
    if topMenu:
        currentItem += '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#">'
        #add the icon
        currentItem += '<i class="fa {} fa-fw"></i><i class="fa fa-caret-down"></i>'.format(iconClass)
        #add the class
        currentItem += '</a><ul class="dropdown-menu {}">'.format(itemClass)
        #now process children
        for child in children:
            # For each child item, provide the parameters it defines to this
            # function, incrementing the depth
            if childrenIconClass:
                child['childrenIconClass'] = childrenIconClass
            else:
                child['childrenIconClass'] = 'fa-dot-circle-o'
            currentItem += dropdown_item(request,currentItem,**child)
        #close the tags
        currentItem += '</ul></li>'

    elif divider:
        currentItem += '<li class="divider"></li>'

    elif section:
        currentItem += '<li class="dropdown-section">'
        #add icon
        currentItem += '<i class="fa {} fa-fw"></i>'.format(iconClass)
        #add section name
        currentItem += '{}</li>'.format(text)

    elif title:
        currentItem += '<div class="dropdown-title">{}</div>'.format(text)

    else:
        #add link
        currentItem += '<li><a href="{}">'.format(link)
        #add icon
        if iconClass:
            itemIcon = iconClass
        else:
            itemIcon = childrenIconClass
        currentItem += '<i class="fa {} fa-fw">'.format(itemIcon)
        #add name
        currentItem += '</i> {}</a></li>'.format(text)

    return currentItem
