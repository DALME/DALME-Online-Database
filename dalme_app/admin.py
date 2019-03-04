"""
This file is where all of the admin interface views are set up, available at
/admin
"""

from django.contrib import admin

from .models import (par_inventory, par_folio, par_token, par_object,
    Notification, Agent, Attribute_type, Attribute, Attribute_DATE,
    Attribute_DBR, Attribute_INT, Attribute_STR, Attribute_TXT, Concept,
    Content_class, Content_type, Content_type_x_attribute_type, Headword,
    Object, Object_attribute, Place, Source, Page, Transcription,
    Identity_phrase, Object_phrase, Wordform, Token,
    Identity_phrase_x_entity)

class DalmeBaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_username = request.user.username
        obj.modification_username = request.user.username
        obj.save()

admin.site.register(par_inventory)
admin.site.register(par_folio)
admin.site.register(par_token)
admin.site.register(par_object)
admin.site.register(Notification)
admin.site.register(Agent)
admin.site.register(Attribute_type)
admin.site.register(Attribute)
admin.site.register(Attribute_DATE)
admin.site.register(Attribute_DBR)
admin.site.register(Attribute_INT)
admin.site.register(Attribute_STR)
admin.site.register(Attribute_TXT)
admin.site.register(Concept)
admin.site.register(Content_class)
admin.site.register(Content_type)
admin.site.register(Content_type_x_attribute_type)
admin.site.register(Headword)
admin.site.register(Object)
admin.site.register(Object_attribute)
admin.site.register(Place)
admin.site.register(Source)
admin.site.register(Page)
admin.site.register(Transcription)
admin.site.register(Identity_phrase)
admin.site.register(Object_phrase)
admin.site.register(Wordform)
admin.site.register(Token)
admin.site.register(Identity_phrase_x_entity)
