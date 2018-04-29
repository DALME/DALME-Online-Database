from django.contrib import admin
from .models import par_inventories, par_folios, par_tokens, par_objects, error_messages, agents, attribute_types, attributes, attributes_DATE, attributes_DBR, attributes_INT, attributes_STR, attributes_TXT, concepts, content_classes, content_types, content_types_x_attribute_types, headwords, objects, object_attributes, places, sources, pages, transcriptions, identity_phrases, object_phrases, word_forms, tokens, identity_phrases_x_entities

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
admin.site.register(agents)
admin.site.register(attribute_types)
admin.site.register(attributes)
admin.site.register(attributes_DATE)
admin.site.register(attributes_DBR)
admin.site.register(attributes_INT)
admin.site.register(attributes_STR)
admin.site.register(attributes_TXT)
admin.site.register(concepts)
admin.site.register(content_classes)
admin.site.register(content_types)
admin.site.register(content_types_x_attribute_types)
admin.site.register(headwords)
admin.site.register(objects)
admin.site.register(object_attributes)
admin.site.register(places)
admin.site.register(sources)
admin.site.register(pages)
admin.site.register(transcriptions)
admin.site.register(identity_phrases)
admin.site.register(object_phrases)
admin.site.register(word_forms)
admin.site.register(tokens)
admin.site.register(identity_phrases_x_entities)
