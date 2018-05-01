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

    #first map the columns to the corresponding data-types
    #get column headers
    cols = list(df.columns.values)
    #and adjust for the ones that are imported directly to the sources table, i.e. the first 6 columns
    cols = cols[6:]
    output_list = []
    data_types = []

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

        source = sources(
            id = uuid.UUID(row['id']).hex,
            type = int(row['type']),
            name = row['name'],
            short_name = row['short_name'],
            parent_source = uuid.UUID(row['parent_source']).hex,
            is_inventory = is_inv,
            creation_username=username,
            modification_username=username
            )
        source.save()

        #now the attributes
        for a in data_types:
            att = a[0]
            if not pd.isnull(row[att]):
                att_value = row[att]
                atype = a[1]
                dtype = a[2]

                attribute = attributes(
                    attribute_type = int(atype),
                    content_id = uuid.UUID(row['id']).hex
                )
                attribute.save()
                att_id = attribute.id

                if dtype == 'INT':
                    att_value = attributes_INT(
                        attribute_id = att_id,
                        value = int(att_value)
                    )
                    att_value.save()

                elif dtype == 'STR':
                    att_value = attributes_STR(
                        attribute_id = att_id,
                        value = att_value
                    )
                    att_value.save()

                elif dtype == 'TXT':
                    att_value = attributes_TXT(
                        attribute_id = att_id,
                        value = att_value
                    )
                    att_value.save()

                elif dtype == 'DBR':
                    att_value = attributes_DBR(
                        attribute_id = att_id,
                        value = uuid.UUID(att_value).hex
                    )
                    att_value.save()

                elif dtype == 'DATE':
                    #assemble date elements
                    if '_date_day' in att:
                        d_base = att.replace('_date_day','')
                        d_day = row[att]
                        d_month = row[dbase + '_date_month']
                        d_year = row[dbase + '_date_year']
                        d_date = functions.get_date_from_elements(d_day, d_month, d_year)

                        att_value = attributes_DATE(
                            attribute_id = att_id,
                            value_day = int(d_day),
                            value_month = int(d_month),
                            value_year = int(d_year),
                            value = d_date
                        )

    output = output_list
    #output = df.to_html()
    return output
