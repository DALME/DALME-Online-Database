from dalme_app.models import *

# fix duplicate credits before adding constraint to db
# def step_1():
#     credits = Source_credit.objects.all()
#     dup_list = []
#     for credit in credits:
#         self_set = Source_credit.objects.filter(source=credit.source, agent=credit.agent, type=credit.type)
#         if self_set.count() > 1:
#             dup_list.append(credit.source.id)
#             self_set[0].delete()
#
#             # for i in range(self_set.count() - 2):
#             #     self_set[i].delete()
#     print(len(dup_list))
#     return 'Duplicate credits fixed.'


# create content_attribute records necessary to support bibliographic record parents
# set get_current_user in models _templates to return User.objects.get(pk=1)
def step_2():
    for i in range(1, 13):
        at = Attribute_type.objects.get(pk=15)
        ct = Content_type.objects.get(pk=i)
        obj, created = Content_attributes.objects.get_or_create(attribute_type=at, content_type=ct, defaults={'unique': False})
        if not created:
            obj.unique = False
            obj.save()
    return 'Content_Attributes set.'


# amend parent types in content types
def step_3():
    obj = Content_type.objects.get(pk=13)
    obj.parents = '1,2,3,4,5,6,7,11,12'
    obj.save()
    return 'Record content type updated.'


# delete all bibliographic sources
def step_4():
    sources = Source.objects.filter(type__lt=12)
    sources.delete()
    return 'Bibliographic sources deleted.'


# create zotero attribute
def step_5():
    att_type = Attribute_type()
    att_type.name = 'Zotero Key'
    att_type.short_name = 'zotero_key'
    att_type.description = 'Relates a source record to a unique key in the DALME Zotero Library'
    att_type.data_type = 'STR'
    att_type.source = 'DALME'
    att_type.save()

    for i in range(1, 11):
        ct = Content_type.objects.get(pk=i)
        Content_attributes.objects.create(content_type=ct, attribute_type=att_type)


    return 'Zotero attribute created. Remember to update preferences!'
