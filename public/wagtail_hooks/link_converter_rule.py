"""Change link converter rules to enable saved search and reference add-ons."""

# from public.extensions import LINK_FROM_RULES_REGISTER, LINK_HANDLERS_REGISTER, link_entity_decorator

# def link_converter_rule(features):
#     del features.converter_rules_by_converter['contentstate']['link']
#     features.register_converter_rule(
#         'contentstate',
#         'link',
#         {
#             'from_database_format': {
#                 'a[href]': ExternalLinkElementHandler('LINK'),
#                 'a[linktype="page"]': PageLinkElementHandler('LINK'),
#                 'a[linktype="saved_search"]': SavedSearchElementHandler('LINK'),
#                 # 'a[linktype="biblio_entry"]': ReferenceElementHandler('LINK'),
#             },
#             'to_database_format': {
#                 'entity_decorators': {'LINK': link_entity_decorator},
#             },
#         },
#     )
#     features.register_link_type(SavedSearchLinkHandler)
#     # features.register_link_type(ReferenceLinkHandler)
import re

from draftjs_exporter.dom import DOM

UUIDv4 = r'^[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-4[0-9A-Fa-f]{3}-[89ABab][0-9A-Fa-f]{3}-[0-9A-Fa-f]{12}$'


def link_entity_decorator(props):
    id_ = props.get('id')
    link_props = {}

    if id_ is not None and id_ != '':
        if str(id_).isdigit():
            link_props['linktype'] = 'page'
        elif re.fullmatch(UUIDv4, id_):
            link_props['linktype'] = 'saved_search'
        # else:
        #     link_props['linktype'] = 'reference'

        link_props['id'] = id_

    else:
        link_props['href'] = props.get('url')

    return DOM.create_element('a', link_props, props['children'])


def link_converter_rule(features):
    # change converter rules
    from_rules = features.converter_rules_by_converter['contentstate']['link'].get('from_database_format', {})
    # for ruleset in LINK_FROM_RULES_REGISTER:
    #     from_rules[ruleset[0]] = ruleset[1]
    del features.converter_rules_by_converter['contentstate']['link']
    features.register_converter_rule(
        'contentstate',
        'link',
        {
            'from_database_format': from_rules,
            'to_database_format': {
                'entity_decorators': {'LINK': link_entity_decorator},
            },
        },
    )
    # register handlers
    # for link_handler in LINK_HANDLERS_REGISTER:
    #     features.register_link_type(link_handler)
