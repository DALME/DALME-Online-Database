"""
This file is where all of the admin interface views are set up, available at
/admin
"""

from django.contrib import admin

from .models import (par_inventories, par_folios, par_tokens, par_objects,
    error_messages, Agents, Attribute_types, Attributes, Attributes_DATE,
    Attributes_DBR, Attributes_INT, Attributes_STR, Attributes_TXT, Concepts,
    Content_classes, Content_types, Content_types_x_attribute_types, Headwords,
    Objects, Object_attributes, Places, Source, Pages, Transcriptions,
    Identity_phrases, Object_phrases, Word_forms, Tokens,
    Identity_phrases_x_entities)

class DalmeBaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_username = request.user.username
        obj.modification_username = request.user.username
        obj.save()

admin.site.register(par_inventories)
admin.site.register(par_folios)
admin.site.register(par_tokens)
admin.site.register(par_objects)
admin.site.register(error_messages)
admin.site.register(Agents)
admin.site.register(Attribute_types)
admin.site.register(Attributes)
admin.site.register(Attributes_DATE)
admin.site.register(Attributes_DBR)
admin.site.register(Attributes_INT)
admin.site.register(Attributes_STR)
admin.site.register(Attributes_TXT)
admin.site.register(Concepts)
admin.site.register(Content_classes)
admin.site.register(Content_types)
admin.site.register(Content_types_x_attribute_types)
admin.site.register(Headwords)
admin.site.register(Objects)
admin.site.register(Object_attributes)
admin.site.register(Places)
admin.site.register(Source)
admin.site.register(Pages)
admin.site.register(Transcriptions)
admin.site.register(Identity_phrases)
admin.site.register(Object_phrases)
admin.site.register(Word_forms)
admin.site.register(Tokens)
admin.site.register(Identity_phrases_x_entities)
