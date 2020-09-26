from dalme_app.models import *
from django.contrib.auth.models import User, Group

# 0. Temporarily change middleware in model_templates
#           return User.objects.get(pk=1)

# 1. run commands

# 2. deal with file units without parent:
#    The register of Crest (1404-1409) (Smail)  MISC_SMAIL
#    Llabres edition

# 3. review:
#   a. permissions assigned to each group in Django admin
#   b. permissions assigned to each group in Wagtail admin
#   c. SAML group assignations in DAM
#   d. groups in Wiki.js
#   e. users primary group


def run_commands():
    entrysets = [
        {
            'group': {
                'id': 14,
                'name': 'Équipe Ferrand',
                'description': 'Grants access to sources added by Guilhem Ferrand.',
                'type': 3
            },
            'dataset': {
                'name': 'Ferrand Sources',
                'description': 'Contains sources added by Guilhem Ferrand.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'AD Aveyron'
            ]
        },
        {
            'group': {
                'name': 'Équipe Saussus',
                'description': 'Grants access to sources added by Lise Saussus.',
                'type': 3
            },
            'dataset': {
                'name': 'Saussus Sources',
                'description': 'Contains sources added by Lise Saussus.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'ADN'
            ],
            'members': [56]
        },
        {
            'group': {
                'id': 12,
                'name': 'Squadra LOC-GLOB',
                'description': 'Grants access to sources added by the LOC-GLOB team.',
                'type': 3
            },
            'dataset': {
                'id': '15ecfc2e-6043-4e85-bed1-5f6b2f26c62f',
                'name': 'LOC-GLOB Sources',
                'description': 'Contains sources added by the LOC-GLOB team.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'ACBormio', 'ASBg', 'ASCM', 'ASOM', 'ASSo', 'ASTo'
            ],
            'members': [58, 57]
        },
        {
            'group': {
                'name': 'Squadra Seche',
                'description': 'Grants access to sources added by Giuseppe Seche.',
                'type': 3
            },
            'dataset': {
                'name': 'Seche Sources',
                'description': 'Contains sources added by Giuseppe Seche.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'AS Pisa', 'ASCa'
            ]
        },
        {
            'group': {
                'name': 'Équipe Laumonier',
                'description': 'Grants access to sources added by Lucie Laumonier.',
                'type': 3
            },
            'dataset': {
                'name': 'Laumonier Sources',
                'description': 'Contains sources added by Lucie Laumonier.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'AD Hérault'
            ]
        },
        {
            'group': {
                'name': 'Harvard Team',
                'description': 'Grants access to sources added by the Harvard DALME team.',
                'type': 3
            },
            'dataset': {
                'name': 'Harvard Sources',
                'description': 'Contains sources added by the Harvard DALME team.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'ACSG', 'ACU', 'AD Haute Garonne', 'ADBR', 'AMM', 'AN', 'AS Bologna', 'AS Messina', 'ASF', 'ASGe', 'ASL', 'BHSA', 'GStA'
            ],
            'members': [1, 5, 35, 36, 37, 38, 52, 64]
        },
        {
            'group': {
                'name': 'Team Lester-Morreale',
                'description': 'Grants access to sources added by Anne Lester and Laura Morreale.',
                'type': 3
            },
            'dataset': {
                'name': 'Lester-Morreale Sources',
                'description': 'Contains sources added by Anne Lester and Laura Morreale.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'AD Somme'
            ],
            'members': [35]
        },
        {
            'group': {
                'name': 'Equipo Belenguer',
                'description': 'Grants access to sources added by Antonio Belenguer.',
                'type': 3
            },
            'dataset': {
                'id': '002edb8f-7fd2-433a-b5d6-df8def749cee',
                'name': 'Belenguer Sources',
                'description': 'Contains sources added by Antonio Belenguer.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'APPV', 'AR Mallorca', 'AR València'
            ]
        },
        {
            'group': {
                'id': 13,
                'name': 'Hinds Team',
                'description': 'Grants access to sources added by Sarah Hinds.',
                'type': 3
            },
            'dataset': {
                'id': '5ef056a0-b060-4b5e-9f66-5e05434d7352',
                'name': 'Hinds Sources',
                'description': 'Contains sources added by Sarah Hinds.',
                'set_type': 3,
                'endpoint': 'sources',
                'permissions': 2
            },
            'archives': [
                'TNA'
            ],
            'members': [65]
        },
        {
            'group': {
                'id': 1,
                'name': 'Super Administrators',
                'description': 'DB: reserved group that provides full system access.',
                'type': 1
            }
        },
        {
            'group': {
                'id': 5,
                'name': 'Administrators',
                'description': 'General: members have access to admin backends in DB, DAM, Knowledge Base, and Public website. They pass most regular permissions checks.',
                'type': 1
            }
        },
        {
            'group': {
                'id': 2,
                'name': 'Developers',
                'description': 'DB: Special group reserved for backend system access.',
                'type': 1
            }
        },
        {
            'group': {
                'id': 7,
                'name': 'Web Editors',
                'description': 'Public Website: members can see most content and approve pages for publication.',
                'type': 5
            }
        },
        {
            'group': {
                'id': 8,
                'name': 'Editors',
                'description': 'DB: members can perform limited editorial tasks, such as managing lists (locales, countries, languages).',
                'type': 1
            }
        },
        {
            'group': {
                'id': 4,
                'name': 'Users',
                'description': 'DB: members can log-in, add and work on their own content, and view other content not marked as private.',
                'type': 1
            }
        },
        {
            'group': {
                'id': 10,
                'name': 'DAM Editors',
                'description': 'DAM: members can add, edit, and delete most content.',
                'type': 2
            }
        },
        {
            'group': {
                'id': 11,
                'name': 'DAM Users',
                'description': 'DAM: members can search and view content, as well as create their own private collections.',
                'type': 2
            }
        },
        {
            'group': {
                'name': 'KB Users',
                'description': 'Knowledge Base: members can view and create content.',
                'type': 4
            }
        },
        {
            'group': {
                'name': 'Web Users',
                'description': 'Public Website: members can only see their own content and create new pages (which must be approved by an editor before publication).',
                'type': 5
            }
        },
    ]
    remove_groups = [3, 6, 9, 15, 16]
    remove_datasets = ['16226133-b1a0-4ecc-8905-39a4e8cb4751', 'd6398755-524b-4848-8cd9-c0a6838e840c']

    print('Starting:')

    orphans = Source.objects.filter(type=12, parent=None)
    archives = Source.objects.filter(type=19)
    for orphan in orphans:
        for archive in archives:
            if archive.short_name in orphan.short_name:
                orphan.parent = archive
                orphan.save()

    # misspelt outliers: AS Messsina, AR Mallorce, AS Genova,
    outliers = {
        'c81bfda4-0ccd-483d-bc95-9d2d469c2f05': '125938f6-66ce-4dfa-a8cd-59d7e09e2dc0',
        '6e04c235-aebe-4ec5-a616-34a072df09f2': 'ad3cf1d7-a288-4075-86d5-76376e0ea0fd',
        '1a563c65-101d-4aa9-9dc7-44ee26e6110c': '539c24f3-0d27-4484-873b-a55d8c3608ce',
        '48c5eb56-daaf-4c5c-b4bc-22fa46088501': '2dbbbdfa-6689-4485-a07a-61e3c1ac55e9',
        '7114567b-d067-43a2-91d7-f4bf7f76b4b3': '7a902e65-9259-464a-8312-9020c96ebaa5',
    }
    for k, v in outliers.items():
        obj = Source.objects.get(pk=k)
        obj.parent = Source.objects.get(pk=v)
        obj.save()

    print('Orphans fixed')

    for entry in entrysets:
        if entry['group'].get('id') is not None:
            group = Group.objects.get(pk=entry['group']['id'])
            group.name = entry['group']['name']
            group.save()
            properties = group.properties
            properties.type = entry['group']['type']
            properties.description = entry['group']['description']
            properties.save()
        else:
            group = Group()
            group.name = entry['group']['name']
            group.save()
            GroupProperties.objects.create(group=group, type=entry['group']['type'], description=entry['group']['description'])

        print('Group processed')

        if entry.get('dataset') is not None:
            entry['dataset']['dataset_usergroup'] = group
            if entry['dataset'].get('id') is not None:
                dataset = Set.objects.get(pk=entry['dataset'].pop('id'))
                for attr, value in entry['dataset'].items():
                    setattr(dataset, attr, value)
                dataset.save()
            else:
                dataset = Set(**entry['dataset'])
                dataset.save()

            print('Dataset processed')

        if entry.get('archives') is not None:
            for archive in entry['archives']:
                fus = Source.objects.filter(type=12, parent__short_name=archive)
                for fu in fus:
                    fu.primary_dataset = dataset
                    fu.save()

            print('Archives processed')

        if entry.get('members') is not None:
            for member in entry['members']:
                user = User.objects.get(pk=member)
                user.groups.add(group.id)
                profile = user.profile
                profile.primary_group = group
                profile.save()

            print('Members processed')

    for group in remove_groups:
        obj = Group.objects.get(pk=group)
        obj.delete()

    print('Groups removed')

    for set in remove_datasets:
        if Set.objects.filter(pk=set).exists():
            obj = Set.objects.get(pk=set)
            obj.delete()
        else:
            print('Failed to delete ' + str(set))

    print('Sets removed')

    sources = Source.objects.filter(type=13)
    for source in sources:
        if source.parent is not None and source.parent.primary_dataset is not None:
            source.primary_dataset = source.parent.primary_dataset
            source.save()

    print('Records updated with new primary dataset information')

    return 'Done'
