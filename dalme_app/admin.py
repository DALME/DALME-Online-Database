from django.contrib import admin

from .models import external_lemma_attributes, phrases, source_attributes, superlemma_components, concept_components, tokens, predicate_labels, references, reference_attributes, repository_attributes

class DalmeBaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_username = request.user.username
        obj.modification_username = request.user.username
        obj.save()

class external_lemma_attributesAdmin(DalmeBaseAdmin):
	fields = ('subject','predicate','object')

class phrasesAdmin(DalmeBaseAdmin):
	fields = ('parent_phrase','type','platonic_concept')

class source_attributesAdmin(DalmeBaseAdmin):
	fields = ('subject','predicate','object','comments')

class superlemma_componentsAdmin(DalmeBaseAdmin):
	fields = ('subject','predicate','object')

class concept_componentsAdmin(DalmeBaseAdmin):
	fields = ('subject','predicate','object')

class tokensAdmin(DalmeBaseAdmin):
	fields = ('token','line')

class predicate_labelsAdmin(DalmeBaseAdmin):
	fields = ('predicate','language','label')

class referencesAdmin(DalmeBaseAdmin):
	fields = ('foreign_id','type','source_id','comments')

class reference_attributesAdmin(DalmeBaseAdmin):
    fields = ('subject','predicate','object')

class repository_attributesAdmin(DalmeBaseAdmin):
    fields = ('subject','predicate','object')


admin.site.register(external_lemma_attributes, external_lemma_attributesAdmin)
admin.site.register(phrases, phrasesAdmin)
admin.site.register(source_attributes, source_attributesAdmin)
admin.site.register(superlemma_components, superlemma_componentsAdmin)
admin.site.register(concept_components, concept_componentsAdmin)
admin.site.register(tokens, tokensAdmin)
admin.site.register(predicate_labels, predicate_labelsAdmin)
admin.site.register(references, referencesAdmin)
admin.site.register(reference_attributes, reference_attributesAdmin)
admin.site.register(repository_attributes, repository_attributesAdmin)
