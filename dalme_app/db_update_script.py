import re
import os
import json
import pandas as pd
from dalme_app.models import *
from datetime import date
from django.contrib.auth.models import User

# IMPORTANT NOTES:
#
# login in shell:
# from django.contrib.auth import authenticate
# authenticate(username = 'pizzorno', password = '****')
# def get_current_user():
#   return user
#
# BEFORE RUNNING:
# Change back model fields in LanguageReference!

def get_current_user():
    return user

def update_db():
    print(update_language_model())
    print(update_attribute_fk_types())
    print(update_language_attributes())
    return "All tasks completed."


def set_multi_attributes_content():
    changes = [
        {'attribute_type_id': 36, 'content_type_id': 13},
        {'attribute_type_id': 15, 'content_type_id': 13},
        {'attribute_type_id': 36, 'content_type_id': 12},
        {'attribute_type_id': 15, 'content_type_id': 12},
    ]
    for change in changes:
        target = Content_attributes.objects.get(attribute_type=change['attribute_type_id'], content_type=change['content_type_id'])
        target.unique = False
        target.save()
    return "Multi-attribute content types updated."


def update_language_model():
    languages = LanguageReference.objects.all()
    for lang in languages:
        if lang.type == 'language':
            lang.lang_type = 1
        elif lang.type == 'dialect':
            lang.lang_type = 2
        lang.save()
    return "Language model updated. TO DO: Remove type field from model and rename lang_type => type."


def update_attribute_fk_types():
    targets = Attribute_type.objects.filter(data_type='UUID')
    for target in targets:
        target.data_type = 'FK-UUID'
        target.save()
    return "Attribute FK types updated."


def update_language_attributes():
    atype = Attribute_type.objects.get(pk=15)
    atype.data_type = 'FK-INT'
    atype.save()

    targets = Attribute.objects.filter(attribute_type=15)
    lang_dict = {
        'ca': 32,
        'de': 71,
        'en': 511,
        'fr': 54,
        'it': 76,
        'la': 618
    }
    for target in targets:
        if len(target.value_STR) == 3:
            lang_id = LanguageReference.objects.get(iso6393=target.value_STR).id
        else:
            lang_id = lang_dict[target.value_STR]
        str_value = {
            'class': 'LanguageReference',
            'id': str(lang_id)
        }
        target.value_STR = json.dumps(str_value)
        target.save()
    return "Language attributes updated. TO DO: Change language attribute type to FK-INT."


def update_city_attributes():
    # update type
    atype = Attribute_type.objects.get(pk=36)
    atype.name = 'Locale'
    atype.short_name = 'locale'
    atype.data_type = 'FK-INT'
    atype.save()

    problems = []
    targets = Attribute.objects.filter(attribute_type=36)
    for target in targets:
        value = LocaleReference.objects.filter(name=target.value_STR)
        if value.count() == 1:
            value = value[0]
            str_value = {
                'class': 'LocaleReference',
                'id': str(value.id)
            }
            target.value_STR = json.dumps(str_value)
            target.save()
        else:
            problems.append(target.id)
    return "City attributes update complete. Problems: " + str(problems)


def update_country_attributes():
    # update type
    atype = Attribute_type.objects.get(pk=62)
    atype.data_type = 'FK-INT'
    atype.save()

    targets = Attribute.objects.filter(attribute_type=62)
    for target in targets:
        value = CountryReference.objects.get(name=target.value_STR)
        str_value = {
            'class': 'CountryReference',
            'id': str(value.id)
        }
        target.value_STR = json.dumps(str_value)
        target.save()
    return "Country attributes updated"

# must be executed in normal RR-cycle
def create_agents_from_users():
    users = User.objects.all()
    problems = []
    for user in users:
        new_agent = Agent()
        new_agent.standard_name = user.profile.full_name
        new_agent.type = 1
        new_agent.user = user
        new_agent.save()
    return 'Agents created - problems: ' + str(problems)
