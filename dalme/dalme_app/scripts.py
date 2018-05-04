import re, json, requests, hashlib, os, uuid
import pandas as pd
from django.contrib import messages
from .models import par_inventories, par_folios, par_tokens, par_objects, error_messages, agents, attribute_types, attributes, attributes_DATE, attributes_DBR, attributes_INT, attributes_STR, attributes_TXT, concepts, content_classes, content_types, content_types_x_attribute_types, headwords, objects, object_attributes, places, sources, pages, transcriptions, identity_phrases, object_phrases, word_forms, tokens, identity_phrases_x_entities
from django.contrib.auth.models import User
from async_messages import message_user
from dalme_app import functions

def import_sources_csv(username):
    _file = 'sources_final.csv'
    _file = os.path.join('dalme','dalme_app',_file)
    df = pd.read_csv(_file)

    #first map the columns to the corresponding data-types
    #get column headers
    cols = list(df.columns.values)
    #and adjust for the ones that are imported directly to the sources table, i.e. the first 6 columns
    cols = cols[6:]
    data_types = []
    new_sources = []
    new_attributes = []
    new_attributes_INT = []
    new_attributes_STR = []
    new_attributes_TXT = []
    new_attributes_DBR = []
    new_attributes_DATE = []

    for c in cols:
        if '-2' in c:
            c = c.replace('-2','')

        entry = attribute_types.objects.get(short_name=c)
        dtype = entry.data_type
        atype = entry.id
        data_types.append((c,atype,dtype))

    #now loop through the rows and create the records
    for i, row in df.iterrows():

        #first create source record in database
        if int(row['is_inventory']) == 1:
            is_inv = True
        else:
            is_inv = False

        #create a new object of "source" type and add the relevant fields
        new_source = sources()
        new_source.id = uuid.UUID(row['id']).hex
        new_source.type = int(row['type'])
        new_source.name = row['name']
        new_source.short_name = row['short_name']
        new_source.parent_source = uuid.UUID(row['parent_source']).hex
        new_source.is_inventory = is_inv
        new_source.creation_username = username
        new_source.modification_username = username
        #now append it to the list of new sources
        new_sources.append(new_source)

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

        #now the attributes
        for a in data_types:
            att = a[0]
            if not pd.isnull(row[att]):
                att_value = row[att]
                atype = a[1]
                dtype = a[2]

                new_attribute = attributes()
                new_attribute.attribute_type = int(atype)
                new_attribute.content_id = uuid.UUID(row['id']).hex
                new_attribute.creation_username = username
                new_attribute.modification_username = username
                new_attributes.append(new_attribute)

                #attribute = attributes(
                #    attribute_type = int(atype),
                #    content_id = uuid.UUID(row['id']).hex,
                #    creation_username=username,
                #    modification_username=username
                #)
                #attribute.save()
                #att_id = attribute.id

                if dtype == 'INT':
                    new_att_INT = attributes_INT()
                    new_att_INT.attribute_id = new_attribute
                    new_att_INT.value = int(att_value)
                    new_att_INT.creation_username = username
                    new_att_INT.modification_username = username
                    new_attributes_INT.append(new_att_INT)

                    #att_value = attributes_INT(
                    #    attribute_id = attribute,
                    #    value = int(att_value),
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'STR':
                    new_att_STR = attributes_STR()
                    new_att_STR.attribute_id = new_attribute
                    new_att_STR.value = att_value
                    new_att_STR.creation_username = username
                    new_att_STR.modification_username = username
                    new_attributes_STR.append(new_att_STR)

                    #att_value = attributes_STR(
                    #    attribute_id = attribute,
                    #    value = att_value,
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'TXT':
                    new_att_TXT = attributes_TXT()
                    new_att_TXT.attribute_id = new_attribute
                    new_att_TXT.value = att_value
                    new_att_TXT.creation_username = username
                    new_att_TXT.modification_username = username
                    new_attributes_TXT.append(new_att_TXT)

                    #att_value = attributes_TXT(
                    #    attribute_id = attribute,
                    #    value = att_value,
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'DBR':
                    new_att_DBR = attributes_DBR()
                    new_att_DBR.attribute_id = new_attribute
                    new_att_DBR.value = uuid.UUID(att_value).hex
                    new_att_DBR.creation_username = username
                    new_att_DBR.modification_username = username
                    new_attributes_DBR.append(new_att_DBR)

                    #att_value = attributes_DBR(
                    #    attribute_id = attribute,
                    #    value = uuid.UUID(att_value).hex,
                    #    creation_username=username,
                    #    modification_username=username
                    #)
                    #att_value.save()

                elif dtype == 'DATE':
                    #assemble date elements
                    if '_date_day' in att:
                        d_base = att.replace('_date_day','')
                        d_day = row[att]
                        d_month = row[d_base + '_date_month']
                        d_year = row[d_base + '_date_year']
                        d_date = functions.get_date_from_elements(d_day, d_month, d_year)

                        new_att_DATE = attributes_DATE()
                        new_att_DATE.attribute_id = new_attribute
                        new_att_DATE.value_day = abs(int(d_day))
                        new_att_DATE.value_month = abs(int(d_month))
                        new_att_DATE.value_year = abs(int(d_year))
                        new_att_DATE.value = d_date
                        new_att_DATE.creation_username = username
                        new_att_DATE.modification_username = username
                        new_attributes_DATE.append(new_att_DATE)

                        #att_value = attributes_DATE(
                        #    attribute_id = attribute,
                        #    value_day = int(d_day),
                        #    value_month = int(d_month),
                        #    value_year = int(d_year),
                        #    value = d_date,
                        #    creation_username=username,
                        #    modification_username=username
                        #)

    #now run bulk_creates on the relevant models
    sources.objects.bulk_create(new_sources)
    attributes.objects.bulk_create(new_attributes)
    attributes_INT.objects.bulk_create(new_attributes_INT)
    attributes_STR.objects.bulk_create(new_attributes_STR)
    attributes_TXT.objects.bulk_create(new_attributes_TXT)
    attributes_DBR.objects.bulk_create(new_attributes_DBR)
    attributes_DATE.objects.bulk_create(new_attributes_DATE)

    output = 'ok'
    return output
