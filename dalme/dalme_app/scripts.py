import re, json, requests, hashlib, os, uuid
import pandas as pd
from django.contrib import messages
from .models import par_inventories, par_folios, par_tokens, par_objects, error_messages, agents, attribute_types, attributes, attributes_DATE, attributes_DBR, attributes_INT, attributes_STR, attributes_TXT, concepts, content_classes, content_types, content_types_x_attribute_types, headwords, objects, object_attributes, places, sources, pages, transcriptions, identity_phrases, object_phrases, word_forms, tokens, identity_phrases_x_entities
from django.contrib.auth.models import User
from async_messages import message_user

def import_sources_csv(username):
    _file = 'sources_final.csv'
    _file = os.path.join('dalme','dalme_app',_file)
    df = pd.read_csv(_file)
    test_list = []
    for i, row in df.iterrows():

        #create source record in database
        if int(row['is_inventory']) == 1:
            is_inv = True
        else:
            is_inv = False

        #source = sources(
        #    id = uuid.UUID(row['id']).hex,
        #    type = int(row['type']),
        #    name = row['name'],
        #    short_name = row['short_name'],
        #    parent_source = uuid.UUID(row['parent_source']).hex,
        #    is_inventory = is_inv,
        #    creation_username=username,
        #    modification_username=username
        #    )
        #source.save()

        #now fill the attributes
        cols = [
            'mk1_identifier',
            'mk2_identifier',
            'alt_identifier',
            'act_type',
            'act_type_phrase',
            'language',
            'language_gc',
            'language_2',
            'language_gc_2',
            'url',
            'archival_series',
            'archival_number',
            'start_date_day',
            'start_date_month',
            'start_date_year',
            'end_date_day',
            'end_date_month',
            'end_date_year',
            'city',
            'dataset',
            'debt_phrase',
            'debt_source',
            'debt_amount',
            'debt_unit',
            'debt_unit_type',
            'comments'
        ]



        for c in cols:
            if not pd.isnull(row[c]):
                attribute = attribute_types.objects.get(short_name=c)
                dtype = attribute.data_type
                test_list.append(dtype)


    output = test_list
    #output = df.to_html()
    return output
