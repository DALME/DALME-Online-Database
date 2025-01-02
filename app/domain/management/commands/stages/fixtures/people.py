"""People-related fixtures."""

# User name concordance for disambiguation.
USER_NAME_CONCORDANCE = {
    'Anne E. Lester': 'Anne Lester',
    'Juan Vicente García Marsilla': 'Juan-Vicente Garcia Marsilla',
    'Juliette Calvarin': 'Jules Calvarin',
    'Pablo Sanahuja Ferrer': 'Pablo Sanahuja',
    'Tobias Pamer': 'Tobias Karl Pamer',
    'Yi Ran Angela Zhang': 'Angela Zhang',
    'Laura Morreale': 'Laura K. Morreale',
}

PEOPLE_PAGE_DATA = {
    'title': 'People',
    'short_title': 'People',
    'header_image_id': 11,
    'slug': 'people',
    'show_in_menus': True,
    'body': [
        {'id': 'eac3c1b6-6724-42af-a039-afef0ca8b880', 'type': 'heading', 'value': 'Project Team'},
        {
            'id': '83f8d736-839d-407b-82ed-90e7ae981ccf',
            'type': 'team_list',
            'value': {
                'mode': 'members',
                'role': '',
                'order': 'name',
                'members': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
            },
        },
        {'id': '61df150f-065e-4c33-b103-e5ae76991cc3', 'type': 'heading', 'value': 'Contributors'},
        {
            'id': '447c0a2f-d127-4937-a72d-bb9644592883',
            'type': 'team_list',
            'value': {'mode': 'role', 'role': '3', 'order': 'name', 'members': []},
        },
        {'id': 'd91180b0-8a60-4c9b-8ed2-4b16fe840bec', 'type': 'heading', 'value': 'Advisory Board'},
        {
            'id': 'c381034b-a89c-4df8-b578-40781dc24044',
            'type': 'text',
            'value': '<p data-block-key="khpxl">The members of the DALME board help convey news about the project to colleagues and students in the field and, in turn, bring potential contributors and resources to our attention.</p>',
        },
        {
            'id': '89294881-07a3-4582-8a86-2733be10b447',
            'type': 'team_list',
            'value': {'mode': 'role', 'role': '4', 'order': 'name', 'members': []},
        },
    ],
}

ROLES = {
    'PI': {
        'role': 'PI',
        'description': 'DALME Principal Investigator.',
    },
    'Project Team': {
        'role': 'Core',
        'description': 'Member of the core project team.',
    },
    'Contributors': {
        'role': 'Contributor',
        'description': 'Occasional contributor to the project.',
    },
    'Advisory Board': {
        'role': 'Board',
        'description': 'Member of the DALME Advisory Board.',
    },
}
