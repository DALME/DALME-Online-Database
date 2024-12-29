"""Pharmacopeias web fixtures."""

from wagtail.rich_text import RichText

SAMPLE_GRADIENTS = [
    {
        'colour_1': '#064e8c80',
        'colour_2': '#114a2880',
        'angle': '125',
        'description': 'Homepage header',
    },
    {
        'colour_1': '#5386a0b3',
        'colour_2': '#3f6544e6',
        'angle': '125',
        'description': 'Project section headers',
    },
    {
        'colour_1': '#63623ab3',
        'colour_2': '#8a4747e6',
        'angle': '125',
        'description': 'About section headers',
    },
]

DEFAULT_SETTINGS = {
    'name': 'HP',
    'short_form': 'HP',
    'tagline': 'Historical Pharmacopeias',
    'search_tagline': 'Collections of Historical Pharmacopeias',
    'explore_tagline': 'Collections of Historical Pharmacopeias',
    'team_profiles_url': '/about/people/',
}

HOME_DATA = {
    'title': 'Historical Pharmacopeias',
    'slug': 'historical-pharmacopeias',
    'body': [
        (
            'text',
            RichText(
                '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>'
            ),
        ),
    ],
    'show_in_menus': True,
}

PROJECT_DATA = {'title': 'Project', 'show_in_menus': True}
ABOUT_DATA = {'title': 'About', 'show_in_menus': True}
PROJECT_FLAT_DATA = [
    {
        'title': 'Overview',
        'citable': False,
        'body': [
            (
                'text',
                RichText(
                    '<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>'
                ),
            ),
        ],
    },
]
ABOUT_FLAT_DATA = [
    {
        'title': 'About HP',
        'body': [
            (
                'text',
                RichText(
                    '<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>'
                ),
            ),
        ],
        'show_contact_form': True,
    },
]
