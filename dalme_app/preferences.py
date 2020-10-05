import json
from dynamic_preferences.types import BooleanPreference, StringPreference, ChoicePreference
from dynamic_preferences.preferences import Section
from dynamic_preferences.registries import global_preferences_registry
from dynamic_preferences.users.registries import user_preferences_registry
from dalme_app.utils import JSONPreference

api_settings = Section('api_settings')
general = Section('general')
interface = Section('interface')
source_editor = Section('source_editor')

# @global_preferences_registry.register
# class SiteTitle(StringPreference):
#     section = general
#     name = 'title'
#     default = 'My site'
#     required = False


# @global_preferences_registry.register
# class MaintenanceMode(BooleanPreference):
#     name = 'maintenance_mode'
#     default = False


@global_preferences_registry.register
class ModelSelectFields(JSONPreference):
    """ Object that stores information about select fields for
    endpoints in the API - used by the Select renderer """
    section = api_settings
    name = 'model_select_fields'
    default = {
        'Group': ['name', 'id', 'description'],
        'Set': ['name', 'id', 'detail_string'],
        'User': ['full_name', 'id'],
        'Agent': ['standard_name', 'id'],
        'Library': ['title', 'key', 'shortTitle', 'itemType']
    }


@user_preferences_registry.register
class HomepageCards(JSONPreference):
    """ Which cards should be included in the homepage? """
    section = interface
    name = 'homepage_cards'
    default = ['my_tasks', 'my_worksets', 'problem_tickets']
    verbose_name = "Homepage cards"
    help_text = "Which cards should be included in the home page?"


@user_preferences_registry.register
class SidebarCollapsed(BooleanPreference):
    """ Collapse the sidebar menu by default? """
    section = interface
    name = 'sidebar_collapsed'
    default = False
    verbose_name = "Collapsed sidebar"
    help_text = "Should the sidebar menu be collapsed or extended by default?"


@user_preferences_registry.register
class RememberColumnVisibility(BooleanPreference):
    """ Remember which columns are visible for lists? """
    section = interface
    name = 'remember_column_visibility'
    default = True
    verbose_name = "Remember column visibility in lists"
    help_text = "Should the system remember whether columns are visible or not in lists?"


@user_preferences_registry.register
class ColumnVisibility(JSONPreference):
    """ Columns visibility preferences """
    section = interface
    name = 'column_visibility'
    default = ''
    verbose_name = "Column visibility"


@user_preferences_registry.register
class RecordsListScope(ChoicePreference):
    """ Default scope of the records list """
    choices = [
        ('own', "My own records."),
        ('team', "My team's records."),
        ('all', "All non-private records.")
    ]
    section = interface
    name = 'records_list_scope'
    default = 'own'
    verbose_name = "Scope of Records list"
    help_text = "What should be the default scope for the Records list?"


@user_preferences_registry.register
class SourceEditorTheme(ChoicePreference):
    """ Default theme """
    choices = [
        ('Chrome', 'Chrome'),
        ('Clouds', 'Clouds'),
        ('XCode', 'XCode'),
        ('Kuroir', 'Kuroir'),
        ('SQL Server', 'SQL Server'),
        ('Clouds Midnight', 'Clouds Midnight'),
        ('Cobalt', 'Cobalt'),
        ('Idle Fingers', 'Idle Fingers'),
        ('Terminal', 'Terminal'),
        ('Tomorrow Night Blue', 'Tomorrow Night Blue'),
    ]
    section = source_editor
    name = 'source_editor_theme'
    default = 'Chrome'
    verbose_name = "Theme"
    help_text = "What should be the default theme for the Source Editor?"


@user_preferences_registry.register
class SourceEditorFontSize(ChoicePreference):
    """ Default font size """
    choices = [
        ('12', '12 pts.'),
        ('14', '14 pts.'),
        ('16', '16 pts.'),
        ('18', '18 pts.'),
    ]
    section = source_editor
    name = 'source_editor_font_size'
    default = '14'
    verbose_name = "Font size"
    help_text = "What should be the default font size for the Source Editor?"


@user_preferences_registry.register
class SourceEditorShowInvisibles(BooleanPreference):
    """ Show invisible charactes? """
    section = source_editor
    name = 'source_editor_show_invisibles'
    default = False
    verbose_name = "Show invisibles"


@user_preferences_registry.register
class SourceEditorHighlightWord(BooleanPreference):
    """ Highlight other instances of the selected word? """
    section = source_editor
    name = 'source_editor_highlight_word'
    default = True
    verbose_name = "Highlight word"


@user_preferences_registry.register
class SourceEditorSoftWrap(BooleanPreference):
    """ Soft wrap lines to screen width? """
    section = source_editor
    name = 'source_editor_soft_wrap'
    default = True
    verbose_name = "Soft wrap"


@user_preferences_registry.register
class SourceEditorShowGuides(BooleanPreference):
    """ Show guides? """
    section = source_editor
    name = 'source_editor_show_guides'
    default = True
    verbose_name = "Show guides"


@user_preferences_registry.register
class SourceEditorShowGutter(BooleanPreference):
    """ Show gutter? """
    section = source_editor
    name = 'source_editor_show_gutter'
    default = True
    verbose_name = "Show gutter"


@user_preferences_registry.register
class SourceEditorShowLineNumbers(BooleanPreference):
    """ Show line numbers? """
    section = source_editor
    name = 'source_editor_show_line_numbers'
    default = True
    verbose_name = "Show line numbers"
