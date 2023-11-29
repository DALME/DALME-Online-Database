from django.contrib.auth import get_user_model

from dalme_app.models import *


def run_commands():
    # 1: create necessary agents
    print(step_1())

    # 2: create necessary users
    print(step_2())

    # 3: update ownership and credits by locale and parents
    print(step_3())

    # 4: update ownership and credits for Toulousain and LOC-GLOB
    print(step_4())

    return 'Done.'


def step_1():
    _agents = [
        'Christine Barnel',
        'Juliette Sibon',
        'Juliette Calvarin',
        'Henri Villard',
        'Walter Ziegler',
        'Andreas Kraus',
        'Pankraz Fried',
        'Vito Vitale',
        'Bianca Fadda',
        'Gabriella Olla Repetto',
        'Philippe Wolff',
        ]

    try:
        for name in _agents:
            Agent.objects.create(standard_name=name, type=1)
        return '1. Agents created'
    except Exception as e:
        return "1. " + str(e)


def step_2():
    _users = [
        {
            'username': 'guilhem.ferrand',
            'first_name': 'Guilhem',
            'last_name': 'Ferrand',
            'email': 'guilhem.ferrand0154@orange.fr',
            'full_name': 'Guilhem Ferrand',
        },
        {
            'username': 'laumo',
            'first_name': 'Lucie',
            'last_name': 'Laumonier',
            'email': 'laumo001@umn.edu',
            'full_name': 'Lucie Laumonier',
        },
        {
            'username': 'anbegon',
            'first_name': 'Antonio',
            'last_name': 'Belenguer González',
            'email': 'anbegon@alumni.uv.es',
            'full_name': 'Antonio Belenguer González',
        },
        {
            'username': 'seche.giuseppe',
            'first_name': 'Giuseppe',
            'last_name': 'Seche',
            'email': 'seche.giuseppe@gmail.com',
            'full_name': 'Giuseppe Seche',
        },
    ]
    try:
        for entry in _users:
            profile = {
                'full_name': entry.pop('full_name'),
            }
            entry['is_superuser'] = False
            entry['is_staff'] = False
            entry['is_active'] = False
            user = get_user_model().objects.create_user(**entry)
            user.save()
            Profile.objects.create(user=user, **profile)
            Agent.objects.create(standard_name=user.profile.full_name, type=1, user=user)
        return '2. Users created'
    except Exception as e:
        return "2. " + str(e)


def step_3():
    ownership = {
        'Marseille': 5,
        'Florence': 35,
        'Aix-en-Provence': 38,
        'Regensburg': 38,
        'Douai': 56,
        'Bologna': 36,
        'Bonifacio': 5,
        # 'Hérault': get_user_model().objects.get(username='laumo').id,
        'Najac': get_user_model().objects.get(username='guilhem.ferrand').id,
        'València': get_user_model().objects.get(username='anbegon').id,
        }

    marseille_editors = {
        'Barnel': 'Christine Barnel',
        'Sibon': 'Juliette Sibon',
        'Calvarin': 'Juliette Calvarin',
        'Low': 'Ryan Low',
        'Casse': 'Henri Villard',
    }

    dls = Agent.objects.get(standard_name='Dan Smail')

    # by city/locale
    for k, v in ownership.items():
        print(k)
        place_id = LocaleReference.objects.get(name=k).id
        print(place_id)
        sources = Attribute.objects.filter(attribute_type=36, value_JSON__id=str(place_id))
        print(sources.count())
        for source in sources:
            obj = source.sources.all()[0]
            obj.owner = get_user_model().objects.get(pk=v)
            obj.save()

            if k == 'Marseille':
                for key, value in marseille_editors.items():
                    if obj.attributes.filter(attribute_type=79, value_TXT__contains=key).exists():
                        agent = Agent.objects.get(standard_name=value)
                        Source_credit.objects.create(source=obj, agent=dls, type=1)
                        Source_credit.objects.create(source=obj, agent=agent, type=1)
                    else:
                        Source_credit.objects.create(source=obj, agent=dls, type=1)

            if k == 'Aix-en-Provence':
                agent = Agent.objects.get(standard_name='Ryan Low')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Regensburg':
                for name in ['Walter Ziegler', 'Andreas Kraus', 'Pankraz Fried']:
                    agent = Agent.objects.get(standard_name=name)
                    Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Douai':
                agent = Agent.objects.get(standard_name='Lise Saussus')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Bologna':
                agent = Agent.objects.get(standard_name='Eric Nemarich')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Bonifacio':
                agent = Agent.objects.get(standard_name='Vito Vitale')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Hérault':
                agent = Agent.objects.get(standard_name='Lucie Laumonier')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Najac':
                agent = Agent.objects.get(standard_name='Guilhem Ferrand')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

            if k == 'Florence':
                agent = Agent.objects.get(standard_name='Laura Morreale')
                Source_credit.objects.create(source=obj, agent=agent, type=1)

    # by parent
    sources = Source.objects.filter(parent__parent__parent='e14cbf38-b53a-4924-bae0-e41f9ad6c307')
    for source in sources:
        source.owner = get_user_model().objects.get(pk=65)
        agent = Agent.objects.get(standard_name='Sarah Hinds')
        Source_credit.objects.create(source=source, agent=agent, type=1)

    sources = Source.objects.filter(parent__parent__parent='2dbbbdfa-6689-4485-a07a-61e3c1ac55e9')
    for source in sources:
        source.owner = get_user_model().objects.get(pk=37)
        agent = Agent.objects.get(standard_name='Patrick Meehan')
        Source_credit.objects.create(source=source, agent=agent, type=1)

    return '3. Ownership and credits (by locale/parent) updated.'


def step_4():
    # Toulousain sources
    t_set = Set()
    t_set.name = 'Toulousain Sources'
    t_set.set_type = 4
    t_set.endpoint = 'sources'
    t_set.permissions = 4
    t_set.owner = get_user_model().objects.get(pk=5)
    t_set.description = 'Autogenerated set for Toulousain sources. Created after removal of fake city attribute.'
    t_set.save()

    sources = Source.objects.filter(parent__parent__id='0a618b8c-6b34-4002-a2f0-d5245e254040')
    for source in sources:
        print(source.id)
        source.owner = get_user_model().objects.get(pk=36)
        agent = Agent.objects.get(standard_name='Philippe Wolff')
        Source_credit.objects.create(source=source, agent=agent, type=1)

        Set_x_content.objects.create(set_id=t_set, content_object=source)

    return '4. Ownership and credits Toulousain updated.'
