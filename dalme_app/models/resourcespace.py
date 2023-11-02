"""Model resourcespace data."""
import hashlib
import json
import os
from urllib.parse import urlencode

import requests

from django.db import models
from django.db.models import options

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


def rs_api_query(**kwargs):
    """Query the ResourceSpace API at dam.dalme.org."""
    endpoint = 'https://dam.dalme.org/api/?'
    user = os.environ['DAM_API_USER']
    key = os.environ['DAM_API_KEY']

    query_params = {
        'function': kwargs.get('function', 'search_get_previews'),
        'param1': kwargs.get('param1', ''),  # search string in RS format
        'param2': kwargs.get('param2', ''),  # string of resource type IDs '1,2'. Empty = all types.
        'param3': kwargs.get(
            'param3',
            '',
        ),  # string indicating results order.
        # Valid options: relevance, popularity, rating, date, colour, country, title, file_path, resourceid, resouretype,
        # titleandcountry, random, status. empty = relevance ordering.
        'param4': kwargs.get('param4', 0),  # archive status of resources to return. 0=live assets
        'param5': kwargs.get('param5', -1),  # maximum number of rows to return. Use '-1' to return all rows.
        'param6': kwargs.get('param6', 'asc'),  # sort order, 'asc'=ascending, 'desc'=descending (default).
        'param7': kwargs.get(
            'param7',
            '',
        ),  # if performing a 'recent' special search, limit the results to resources created in the last n number of days
        'param8': kwargs.get(
            'param8',
            'thm, scr',
        ),  # comma separated list of preview sizes e.g. 'thm, scr'' will retrieve the thumbnail and screen sized previews
        # '' = don't return any preview URLs (default).
        'param9': kwargs.get('param9', 'jpg'),  # Return preview files matching this file extension. e.g. 'mp4', 'jpg'
    }

    sign = hashlib.sha256(key.encode('utf-8'))
    query_params['user'] = user
    paramstr = urlencode(query_params)
    sign.update(paramstr.encode('utf-8'))

    return requests.get(endpoint + paramstr + '&sign=' + sign.hexdigest())


class rs_resource(models.Model):  # noqa: N801
    ref = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, blank=True)
    resource_type = models.IntegerField(null=True)
    has_image = models.IntegerField(default='0')
    is_transcoding = models.IntegerField(default='0')
    hit_count = models.IntegerField(default='0')
    new_hit_count = models.IntegerField(default='0')
    creation_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True)
    user_rating = models.IntegerField(null=True)
    user_rating_count = models.IntegerField(null=True)
    user_rating_total = models.IntegerField(null=True)
    country = models.CharField(max_length=200, blank=True, default=None)
    file_extension = models.CharField(max_length=10, blank=True)
    preview_extension = models.CharField(max_length=10, blank=True)
    image_red = models.IntegerField(null=True)
    image_green = models.IntegerField(null=True)
    image_blue = models.IntegerField(null=True)
    thumb_width = models.IntegerField(null=True)
    thumb_height = models.IntegerField(null=True)
    archive = models.IntegerField(default='0')
    access = models.IntegerField(default='0')
    colour_key = models.CharField(max_length=5, blank=True)
    created_by = models.IntegerField(null=True)
    file_path = models.CharField(max_length=500, blank=True)
    file_modified = models.DateTimeField(null=True, blank=True)
    file_checksum = models.CharField(max_length=32, blank=True)
    request_count = models.IntegerField(default='0')
    expiry_notification_sent = models.IntegerField(default='0')
    preview_tweaks = models.CharField(max_length=50, blank=True)
    geo_lat = models.FloatField(null=True, default=None)
    geo_long = models.FloatField(null=True, default=None)
    mapzoom = models.IntegerField(null=True)
    disk_usage = models.IntegerField(null=True)
    disk_usage_last_updated = models.DateTimeField(null=True, blank=True)
    file_size = models.IntegerField(null=True, default=None)
    preview_attempts = models.IntegerField(null=True, default=None)
    field12 = models.CharField(max_length=200, blank=True, default=None)
    field8 = models.CharField(max_length=200, blank=True, default=None)
    field3 = models.CharField(max_length=200, blank=True, default=None)
    annotation_count = models.IntegerField(null=True)
    field51 = models.CharField(max_length=200, blank=True, default=None)
    field79 = models.CharField(max_length=200, blank=True, default=None)
    modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    collections = models.ManyToManyField('rs_collection', through='rs_collection_resource')

    class Meta:
        managed = False
        db_table = 'resource'
        in_db = 'dam'

    def __str__(self):
        return self.ref

    def get_image_url(self, size='scr'):
        """Return url of image."""
        query_params = {
            'param1': '!list' + str(self.ref),
            'param5': '1',
            'param8': size,
        }
        response = rs_api_query(**query_params)
        data = json.loads(response.text)
        return data[0][f'url_{size}']


class rs_resource_data(models.Model):  # noqa: N801
    django_id = models.IntegerField(primary_key=True, db_column='django_id')
    resource = models.ForeignKey(
        'rs_resource',
        db_column='resource',
        to_field='ref',
        on_delete=models.CASCADE,
        related_name='resource_data',
    )
    resource_type_field = models.ForeignKey(
        'rs_resource_type_field',
        db_column='resource_type_field',
        to_field='ref',
        on_delete=models.CASCADE,
        related_name='resource_data_field',
    )
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'resource_data'
        in_db = 'dam'

    def __str__(self):
        return self.django_id


class rs_collection(models.Model):  # noqa: N801
    ref = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True)
    user = models.IntegerField(null=True)
    created = models.DateTimeField(null=True, blank=True)
    public = models.IntegerField(default='0')
    theme = models.CharField(max_length=100, blank=True)
    theme2 = models.CharField(max_length=100, blank=True)
    theme3 = models.CharField(max_length=100, blank=True)
    allow_changes = models.IntegerField(default='0')
    cant_delete = models.IntegerField(default='0')
    keywords = models.TextField()
    savedsearch = models.IntegerField(null=True)
    home_page_publish = models.IntegerField(null=True)
    home_page_text = models.TextField()
    home_page_image = models.IntegerField(null=True)
    session_id = models.IntegerField(null=True)
    theme4 = models.CharField(max_length=100, blank=True)
    theme5 = models.CharField(max_length=100, blank=True)
    theme6 = models.CharField(max_length=100, blank=True)
    theme7 = models.CharField(max_length=100, blank=True)
    theme8 = models.CharField(max_length=100, blank=True)
    theme9 = models.CharField(max_length=100, blank=True)
    theme10 = models.CharField(max_length=100, blank=True)
    theme11 = models.CharField(max_length=100, blank=True)
    theme12 = models.CharField(max_length=100, blank=True)
    theme13 = models.CharField(max_length=100, blank=True)
    theme14 = models.CharField(max_length=100, blank=True)
    theme15 = models.CharField(max_length=100, blank=True)
    theme16 = models.CharField(max_length=100, blank=True)
    theme17 = models.CharField(max_length=100, blank=True)
    theme18 = models.CharField(max_length=100, blank=True)
    theme19 = models.CharField(max_length=100, blank=True)
    theme20 = models.CharField(max_length=100, blank=True)

    class Meta:
        managed = False
        db_table = 'collection'
        in_db = 'dam'

    def __str__(self):
        return self.ref


class rs_collection_resource(models.Model):  # noqa: N801
    """Django model representation of existing RS table."""

    collection = models.ForeignKey(
        'rs_collection',
        db_column='collection',
        to_field='ref',
        on_delete=models.CASCADE,
        related_name='resources_list',
    )
    resource = models.ForeignKey(
        'rs_resource',
        db_column='resource',
        to_field='ref',
        on_delete=models.CASCADE,
        related_name='collections_list',
    )
    date_added = models.DateTimeField(auto_now_add=True, primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField(null=True)
    use_as_theme_thumbnail = models.IntegerField(null=True)
    purchase_size = models.CharField(max_length=10, blank=True)
    purchase_complete = models.IntegerField(default='0')
    purchase_price = models.FloatField(max_length=10, default='0.00')
    sortorder = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'collection_resource'
        in_db = 'dam'

    def __str__(self):
        return f'{self.resource.ref-{self.collection.ref}}'


class rs_user(models.Model):  # noqa: N801
    DAM_USERGROUPS = (
        (2, 'General User'),
        (4, 'Archivist'),
        (1, 'Administrator'),
        (3, 'Super Admin'),
    )

    ref = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=64, blank=True)
    fullname = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    usergroup = models.IntegerField(null=True, choices=DAM_USERGROUPS)
    last_active = models.DateTimeField(null=True, blank=True)
    logged_in = models.IntegerField(null=True)
    last_browser = models.TextField()
    last_ip = models.CharField(max_length=100, blank=True)
    current_collection = models.IntegerField(null=True)
    accepted_terms = models.IntegerField(default='0')
    account_expires = models.DateTimeField(null=True, blank=True)
    comments = models.TextField()
    session = models.CharField(max_length=50, blank=True)
    ip_restrict = models.TextField()
    search_filter_override = models.TextField()
    password_last_change = models.DateTimeField(null=True)
    login_tries = models.IntegerField(default='0')
    login_last_try = models.DateTimeField(null=True, blank=True)
    approved = models.IntegerField(default='1')
    lang = models.CharField(max_length=11, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    hidden_collections = models.TextField()
    password_reset_hash = models.CharField(max_length=100, blank=True)
    origin = models.CharField(max_length=50, blank=True)
    unique_hash = models.CharField(max_length=50, blank=True)
    wp_authrequest = models.CharField(max_length=50, blank=True)
    csrf_token = models.CharField(max_length=255, blank=True)

    class Meta:
        managed = False
        db_table = 'user'
        in_db = 'dam'

    def __str__(self):
        return self.ref


class rs_resource_type_field(models.Model):  # noqa: N801
    ref = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, blank=True)
    title = models.CharField(max_length=400, blank=True)
    type = models.IntegerField(null=True)  # noqa: A003
    order_by = models.IntegerField(default='0')
    keywords_index = models.IntegerField(default='0')
    partial_index = models.IntegerField(default='0')
    resource_type = models.IntegerField(default='0')
    resource_column = models.CharField(max_length=50, blank=True)
    display_field = models.IntegerField(default='1')
    use_for_similar = models.IntegerField(default='1')
    iptc_equiv = models.CharField(max_length=20, blank=True)
    display_template = models.TextField()
    tab_name = models.CharField(max_length=50, blank=True)
    required = models.IntegerField(default='0')
    smart_theme_name = models.CharField(max_length=200, blank=True)
    exiftool_field = models.CharField(max_length=200, blank=True)
    advanced_search = models.IntegerField(default='1')
    simple_search = models.IntegerField(default='0')
    help_text = models.TextField()
    display_as_dropdown = models.IntegerField(default='0')
    external_user_access = models.IntegerField(default='1')
    autocomplete_macro = models.TextField()
    hide_when_uploading = models.IntegerField(default='0')
    hide_when_restricted = models.IntegerField(default='0')
    value_filter = models.TextField()
    exiftool_filter = models.TextField()
    omit_when_copying = models.IntegerField(default='0')
    tooltip_text = models.TextField()
    regexp_filter = models.CharField(max_length=400, blank=True)
    sync_field = models.IntegerField(null=True)
    display_condition = models.CharField(max_length=400, blank=True)
    onchange_macro = models.TextField()
    field_constraint = models.IntegerField(null=True)
    linked_data_field = models.TextField()
    automatic_nodes_ordering = models.IntegerField(default='0')
    fits_field = models.CharField(max_length=255, blank=True)
    personal_data = models.IntegerField(default='0')

    class Meta:
        managed = False
        db_table = 'resource_type_field'
        in_db = 'dam'

    def __str__(self):
        return self.ref
