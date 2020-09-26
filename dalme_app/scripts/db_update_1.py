import json
from dalme_app.models import *
from django.contrib.auth.models import User

# 1. General database clean-up
# delete the following tables manually:
# corsheaders_corsmodel
# oidc_provider_client
# oidc_provider_client_response_types
# oidc_provider_code
# oidc_provider_responsetype
# oidc_provider_rsakey
# oidc_provider_token
# oidc_provider_userconsent

# 2: Adjust migration/db state:
#   a. delete any migrations after 0154_auto_20200826_1339
#   b. uncomment lang_type, old type, and related options
#   c. run makemigrations
#   d. adjust generated file
#       remove CreateModel = LocaleReference AND DeleteModel = CityReference
#       add:
#           migrations.RenameModel(
#               old_name='CityReference',
#               new_name='LocaleReference',
#           ),
#       change: AddField = localereference country, creation_user, and modification_user to AlterField
#   e. temporarily change middleware in model_templates
#           get_current_user = return 1
#   f. run migrations
#  need to fix attribute id = f7a42ec7d5024e2bbd0ed482c934bacc TYPE = 144
# {"class": "RightsPolicy", "id": "6a394a971f47473abc69a71a16879a54"}

def run_commands():
    # 3: migrate language type data:
    print(step_3())

    # 4: update fk types for attributes
    print(step_4())

    # 5: mark multi-attributes as such in Content_attributes
    print(step_5())

    # 6: migrate language attributes to FK-INT
    print(step_6())

    # 7: migrate city/locale attributes to FK-INT
    print(step_7())

    # 8: migrate country attributes to FK-INT
    print(step_8())

    # 9: delete empty attributes
    print(step_9())

    # 10: update FK- attribute types to JSON field
    print(step_10())

    # 11: create agents from users
    # this may need to be run in normal RR-cycle
    print(step_11())

    # 12: fix record type attributes
    print(step_12())



    return 'Done.'

# 12: fix LanguageReference model
#   a. restore type field and remove old type and lang_type + options
#   b. run makemigrations and change RemoveField lang_type to RenameField and alterfield type to remove
#   c. run migrations

#################################
# 13: RESTORE PROPER RETURN IN get_current_user middleware
#################################


def step_3():
    try:
        languages = LanguageReference.objects.all()
        for lang in languages:
            if lang.type == 'language':
                lang.lang_type = 1
            elif lang.type == 'dialect':
                lang.lang_type = 2
            lang.save()
        return "3. Language type data migrated. TO DO: Remove type field from model and rename lang_type => type."
    except Exception as e:
        return "3. " + str(e)


def step_4():
    try:
        targets = Attribute_type.objects.filter(data_type='UUID')
        for target in targets:
            target.data_type = 'FK-UUID'
            target.save()
        return "4: Attribute types: UUID -> FK-UUID updated."
    except Exception as e:
        return "4. " + str(e)


def step_5():
    try:
        changes = [
            {'attribute_type_id': 36, 'content_type_id': 13},
            {'attribute_type_id': 15, 'content_type_id': 13},
            {'attribute_type_id': 36, 'content_type_id': 12},
            {'attribute_type_id': 15, 'content_type_id': 12},
        ]
        for change in changes:
            ct = Content_type.objects.get(pk=change['content_type_id'])
            at = Attribute_type.objects.get(pk=change['attribute_type_id'])
            target = Content_attributes.objects.get_or_create(attribute_type=at, content_type=ct, defaults={'unique': False})
            if type(target) is tuple:
                target[0].unique = False
                target[0].save()
        return "5. Multi-attribute content types marked."
    except Exception as e:
        return "5. " + str(e)


def step_6():
    try:
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
        return "6. Language attributes updated."
    except Exception as e:
        return "6. " + str(e)


def step_7():
    try:
        # update type
        atype = Attribute_type.objects.get(pk=36)
        atype.name = 'Locale'
        atype.short_name = 'locale'
        atype.data_type = 'FK-INT'
        atype.save()
        problems = []
        targets = Attribute.objects.filter(attribute_type=36)
        for target in targets:
            if LocaleReference.objects.filter(name=target.value_STR).exists():
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
            else:
                # delete records with Tolousain fake locale
                target.delete()
        return "7. Locale attributes update complete. Problems = " + str(problems)
    except Exception as e:
        return "7. " + str(e)


def step_8():
    try:
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
        return "8. Country attributes updated"
    except Exception as e:
        return "8. " + str(e)


def step_9():
    try:
        Attribute.objects.filter(value_STR=None, value_INT=None, value_TXT=None).delete()
        return '9. Empty attributes deleted'
    except Exception as e:
        return "9. " + str(e)


def step_10():
    targets = Attribute_type.objects.filter(data_type='FK-INT')
    for target in targets:
        attributes = Attribute.objects.filter(attribute_type=target)
        for att in attributes:
            val = json.loads(att.value_STR)
            val_str = str(eval('{}.objects.get(pk={})'.format(val['class'], val['id'])))
            att.value_JSON = val
            att.value_STR = val_str
            att.save()

    targets = Attribute_type.objects.filter(data_type='FK-UUID')
    for target in targets:
        attributes = Attribute.objects.filter(attribute_type=target)
        for att in attributes:
            val = json.loads(att.value_STR)
            val_str = str(eval('{}.objects.get(pk=\'{}\')'.format(val['class'], val['id'])))
            att.value_JSON = val
            att.value_STR = val_str
            att.save()

    return '10. FK attributes updated to new JSON type field: TO DO: Uncomment STR lines in Attribute model!'


# must be executed in normal RR-cycle
def step_11():
    users = User.objects.all()
    for user in users:
        try:
            test = (user.profile is not None)
        except:
            user.delete()
    try:
        users = User.objects.all()
        problems = []
        for user in users:
            new_agent = Agent()
            new_agent.standard_name = user.profile.full_name
            new_agent.type = 1
            new_agent.user = user
            new_agent.save()
        return '11. Agents created. TO DO: review records manually. Problems: ' + str(problems)
    except Exception as e:
        return "11. " + str(e)


def step_12():
    conversions = {
        'Inventarium de bonis indefensis': 'Inventory-Undefended Goods',
        'Guradianship': 'Guardianship',
        'Inventory': 'Inventory-Generic',
    }
    try:
        for k, v in conversions.items():
            targets = Attribute.objects.filter(attribute_type=28, value_STR=k)
            if targets.exists():
                for target in targets:
                    if not Attribute.objects.filter(object_id=target.object_id, attribute_type=28, value_STR=v).exists():
                        target.value_STR = v
                        target.save()
                    else:
                        target.delete()
        return '12. Record types fixed'
    except Exception as e:
        return "12. " + str(e)
