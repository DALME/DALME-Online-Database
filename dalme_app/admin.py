from django.contrib import admin

from .models import PlatonicConcept, Relationship, SourceType, SourceAttributeType, Source, SourceAttribute

class DalmeBaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_username = request.user.username
        obj.modification_username = request.user.username
        obj.save()

class PlatonicConceptAdmin(DalmeBaseAdmin):
    fields = ('term','getty_term','comments')

class RelationshipAdmin(DalmeBaseAdmin):
    fields = ('source','relationship','target')

class SourceTypeAdmin(DalmeBaseAdmin):
    fields = ('type_csl','type_zotero','dropdown_content','comments')

class SourceAttributeTypeAdmin(DalmeBaseAdmin):
    fields = ('type_dublin_core','type_csl','type_zotero','dropdown_content','comments')

class SourceAdmin(DalmeBaseAdmin):
    fields = ('dropdown_content','source_type','parent_source','comments')

class SourceAttributeAdmin(DalmeBaseAdmin):
    fields = ('source','type','content','comments')

admin.site.register(PlatonicConcept, PlatonicConceptAdmin)
admin.site.register(Relationship, RelationshipAdmin)
admin.site.register(SourceType, SourceTypeAdmin)
admin.site.register(SourceAttributeType, SourceAttributeTypeAdmin)
admin.site.register(Source, SourceAdmin)
admin.site.register(SourceAttribute, SourceAttributeAdmin)
