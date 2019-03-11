"""
This menus module provides a streamlined way to create menus from simple json files.
"""

from django.contrib.auth.models import User
from django.urls import reverse

import json, os

from . import functions

LEVEL_LOOKUP = ['nav-second-level', 'nav-third-level', 'nav-fourth-level', 'nav-fifth-level']

def menu_constructor(item_constructor, template, state):
    """
    Builds menus based on an item_constructor and a json file describing the menu items.
    Menus are stored in the templates directory, under the menus subdirectory.
    """
    # Declare output string
    _output = ''

    # Get template from default location in dalme_app/templates/menus and read it
    template = os.path.join('dalme_app','templates','menus',template)
    with open(template, 'r') as fp:
        menu = json.load(fp)

    # Create menu by iterating through items in json file and appending to output
    for item in menu:
        _output += eval(item_constructor + '(_output,state,**item)')

    # Return output as part of a list, because renderer expects to iterate
    return [_output]

def sidebar_item(wholeMenu,state,depth=0,text=None,iconClass=None,link=None,counter=None,section=None,children=None,divider=None, itemClass=None, blank=None):
    """
    Generates a menu item and incorporates it into `wholeMenu`. This function
    calls itself to recurse through hierarchies of menus.
    """

    if section:
        currentItem = '<div class="sidebar-heading">{}</div><hr class="sidebar-divider">'.format(text)
    elif divider:
        currentItem = '<hr class="sidebar-divider">'
    else:
        if text in state['breadcrumb']:
            currentItem = '<li class="nav-item active">'
        else:
            currentItem = '<li class="nav-item">'
        if children:
            currentItem += '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapse{}" aria-expanded="true" aria-controls="collapse{}">'.format(itemClass, itemClass)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a>'.format(text)
            if text in state['breadcrumb'] and state['sidebar'] != 'toggled':
                currentItem += '<div id="collapse{}" class="collapse show" aria-labelledby="heading{}" data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            else:
                currentItem += '<div id="collapse{}" class="collapse" aria-labelledby="heading{}" data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            currentItem += '<div class="bg-white py-2 collapse-inner rounded">'
            for child in children:
                currentItem += '<a class="collapse-item'
                if child['text'] in state['breadcrumb']:
                    currentItem += ' active'

                currentItem += '" href="{}"'.format(child['link'])

                if 'blank' in child:
                    currentItem += ' target="_blank"'

                currentItem += '><i class="fas fa-fw {}"></i> {}</a>'.format(child['iconClass'], child['text'])
            currentItem += '</div></div></li>'

        else:
            currentItem += '<a class="nav-link" href="{}">'.format(link)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a></li>'.format(text)

    return currentItem

def tile_item(wholeMenu,state,colourClass=None,iconClass=None,counter=None,counterTitle=None,linkTarget=None,linkTitle=None):

    try:
        counter = functions.get_count(counter)
    except:
        counter = 'n/a'

    currentItem = '<div class="col-xl-3 col-sm-6 mb-3">'
    currentItem += '<div class="card shadow text-dark-grey bg-{}-soft o-hidden h-100"><div class="card-body">'.format(colourClass)
    currentItem += '<div class="card-body-icon"><i class="fas {} fa-comments"></i></div>'.format(iconClass)
    currentItem += '<div class="mr-5"><b>{}</b> {}</div></div>'.format(counter, counterTitle)
    currentItem += '<a class="card-footer text-dark-grey clearfix small z-1" href="{}">'.format(linkTarget)
    currentItem += '<span class="float-left">{}</span>'.format(linkTitle)
    currentItem += '<span class="float-right"><i class="fas fa-angle-right"></i></span></a></div></div>'

    return currentItem

def dropdown_item(wholeMenu,state,topMenu=None,infoPanel=None,title=None,itemClass=None,iconClass=None,childrenIconClass=None,children=None,text=None,link=None,divider=None,section=None,counter=None,circleColour=None,moreText=None,moreLink=None):
    """ creates items for the top right dropdowns """

    currentItem = '<li class="nav-item dropdown no-arrow mx-1">'
    if topMenu:
        currentItem += '<a class="nav-link dropdown-toggle" href="#" id="{}Dropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'.format(itemClass)
        currentItem += '<i class="fas {} fa-fw"></i>'.format(iconClass)
        currentItem += '</a><div class="dropdown-list dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="{}Dropdown">'.format(itemClass)
        currentItem += '<h6 class="dropdown-header">{}</h6>'.format(title)
        for child in children:
            if divider:
                currentItem += '<div class="dropdown-divider"></div>'
            else:
                currentItem += '<a class="dropdown-item" href="{}">'.format(child['link'])
                if 'iconClass' in child:
                    currentItem += '<i class="fas {} fa-sm fa-fw mr-2 text-gray-400"></i>{}</a>'.format(child['iconClass'], child['text'])
                else:
                    currentItem += '<i class="fas {} fa-sm fa-fw mr-2 text-gray-400"></i>{}</a>'.format(childrenIconClass, child['text'])

        currentItem += '</div></li> '

    if infoPanel:
        currentItem += '<a class="nav-link dropdown-toggle" href="#" id="{}Dropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">'.format(itemClass)
        currentItem += '<i class="fas {} fa-fw"></i>'.format(iconClass)
        if counter:
            currentItem += '<span class="badge badge-danger badge-counter">{}</span>'.format(counter)
        currentItem += '</a><div class="dropdown-list dropdown-infopanel dropdown-menu dropdown-menu-right shadow animated--grow-in" aria-labelledby="{}Dropdown">'.format(itemClass)
        currentItem += '<h6 class="dropdown-header">{}</h6>'.format(title)
        for child in children:
            currentItem += '<a class="dropdown-item d-flex align-items-center" href="{}">'.format(child['link'])
            currentItem += '<div class="mr-3"><div class="icon-circle bg-{}"><i class="fas {} text-white"></i></div></div>'.format(child['circleColour'], child['iconClass'])
            currentItem += '<div><div class="small text-gray-500">{}</div><span class="font-weight-bold">{}</span></div></a>'.format(child['small_text'], child['text'])

        currentItem += '<a class="dropdown-item text-center small text-gray-500" href="{}">{}</a></div></li>'.format(moreLink, moreText)

    return currentItem
