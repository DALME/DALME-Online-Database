
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError

from dalme_app.models import *


def run_commands():
    # 1: simple lookups
    # global: <pc force="weak"></pc> -> <pc force="weak">-</pc>
    # global: <del> -> <del rend="overstrike">
    # global: “damaged” -> “damage”
    print(step_1())

    # 2: Florence indents
    # city = Florence -> change all <indent1> to <indent>
    print(step_2())

    # 3: fix attribute data type and delete misplaced record support
    print(step_3())

    # 4: record support
    # global: if record lacks attribute ::support:: -> if parent name contains 'charter' -> 'parchment' else: 'paper'
    print(step_4())

    # 5: fix empty months in data attributes
    print(step_5())

    # 6: fix empty value_STR in attributes
    print(step_6())

    # 7: update dataset membership
    print(step_7())

    # 8: update LOC-GLOB dataset membership
    print(step_8())

    return 'Done.'


def step_1():
    transcriptions = Transcription.objects.all()
    print(f'Starting: {transcriptions.count()} transcriptions to process.')
    count = 0
    for t in transcriptions:
        text = t.transcription
        text = text.replace('<pc force="weak"></pc>', '<pc force="weak">-</pc>')
        text = text.replace('<del>', '<del rend="overstrike">')
        text = text.replace('damaged', 'damage')
        t.transcription = text
        t.save()
        count += 1
        if (count % 100 == 0):
            print(f'{count!s} transcriptions processed.')
    return '1. Simple lookups completed.'


def step_2():
    # city = Florence -> change all <indent1> to <indent>
    place_id = LocaleReference.objects.get(name='Florence').id
    sources = Attribute.objects.filter(attribute_type=36, value_JSON__id=str(place_id))
    for source in sources:
        inv = source.sources.all()[0]
        if inv.pages:
            for fol in inv.pages.all():
                if fol.sources.first().transcription:
                    tr_id = fol.sources.first().transcription.id
                    text = fol.sources.first().transcription.transcription
                    text = text.replace('<hi rend="indent1">', '<hi rend="indent">')
                    Transcription.objects.filter(pk=tr_id).update(transcription=text)

    return '2. Florence indents fixed.'


def step_3():
    # fix attribute type
    a_type = Attribute_type.objects.get(pk=148)
    a_type.data_type = 'STR'
    a_type.save()

    # remove data
    Attribute.objects.filter(attribute_type=148).delete()

    return '3. Data type for support attribute fixed + misplaced records deleted.'


def step_4():
    # global: if record lacks attribute ::support:: -> if parent name contains 'charter' -> 'parchment' else: 'paper'
    records = Source.objects.filter(type=12)
    at = Attribute_type.objects.get(pk=148)
    for record in records:
        if 'charter' in record.name or 'Charter' in record.name:
            Attribute.objects.create(content_object=record, attribute_type=at, value_STR='Parchment')
        else:
            Attribute.objects.create(content_object=record, attribute_type=at, value_STR='Paper')

    return '4. Added support attributes to archival units.'


def step_5():
    date_attributes = [19, 25, 26]
    for da in date_attributes:
        attributes = Attribute.objects.filter(attribute_type=da)
        for att in attributes:
            if att.value_DATE is not None and att.value_DATE_m is None:
                att.value_DATE_m = att.value_DATE.month
                att.value_STR = att.value_DATE.strftime('%d-%b-%Y').lstrip("0").replace(" 0", " ")
    return '5. Date attributes fixed'


def step_6():
    targets = Attribute.objects.filter(value_STR=None)
    print('Targets = ' + str(targets.count()))
    for target in targets:
        try:
            if target.attribute_type.data_type == 'INT' and target.value_INT is not None:
                target.value_STR = str(target.value_INT)
                target.save()
            if target.attribute_type.data_type == 'TXT' and target.value_TXT is not None:
                target.value_STR = target.value_TXT[0:254] if len(target.value_TXT) > 255 else target.value_TXT
                target.save()
        except IntegrityError:
            target.delete()

    return '6. Empty value_STR attributes fixed'


def step_7():
    sources = Source.objects.filter(type=13)
    ct = ContentType.objects.get(pk=125)
    for source in sources:
        if source.primary_dataset is not None:
            if not Set_x_content.objects.filter(set_id=source.primary_dataset, object_id=source.id).exists():
                Set_x_content.objects.create(set_id=source.primary_dataset, object_id=source.id, content_type=ct)
    return '7. Dataset membership updated'


def step_8():
    #LOC-GLOB
    sxcs = Set.objects.get(pk='15ecfc2e-6043-4e85-bed1-5f6b2f26c62f').members.all()
    print(sxcs.count())
    owner = User.objects.get(pk=57)
    for sxc in sxcs:
        obj = sxc.content_object
        obj.owner = owner
        obj.save()

    return '8. Ownership and credits LOC-GLOB updated.'
