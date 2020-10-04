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
    sources = Source.objects.filter(type_lt=12)
    sources.delete()
    return 'Bibliographic sources deleted.'
