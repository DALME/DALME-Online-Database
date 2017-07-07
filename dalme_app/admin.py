from django.contrib import admin

from .models import external_lemmata, external_lemma_attributes, phrases, source_attributes, sources, superlemmata, superlemma_components, concepts, concept_components, inventories, leaves, tokens, inventory_attributes, predicates, predicate_labels, references, repository, reference_attributes, repository_attributes

class DalmeBaseAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_username = request.user.username
        obj.modification_username = request.user.username
        obj.save()

class external_lemmataAdmin(DalmeBaseAdmin):
	fields = ('temp')

class external_lemma_attributesAdmin(DalmeBaseAdmin):
	fields = ('subject', 'predicate', 'object')

class phrasesAdmin(DalmeBaseAdmin):
	fields = ('parent_phrase', 'type', 'platonic_concept')

class source_attributesAdmin(DalmeBaseAdmin):
	fields = ('subject', 'predicate', 'object', 'comments')

class sourcesAdmin(DalmeBaseAdmin):
	fields = ('temp')

class superlemmataAdmin(DalmeBaseAdmin):
	fields = ('temp')

class superlemma_componentsAdmin(DalmeBaseAdmin):
	fields = ('subject', 'predicate', 'object')

class conceptsAdmin(DalmeBaseAdmin):
	fields = ('temp')

class concept_componentsAdmin(DalmeBaseAdmin):
	fields = ('subject', 'predicate', 'object')

class inventoriesAdmin(DalmeBaseAdmin):
	fields = ('temp')

class leavesAdmin(DalmeBaseAdmin):
	fields = ('temp')

class tokensAdmin(DalmeBaseAdmin):
	fields = ('token', 'line')

class inventory_attributesAdmin(DalmeBaseAdmin):
	fields = ('temp')

class predicatesAdmin(DalmeBaseAdmin):
	fields = ('uri')

class predicate_labelsAdmin(DalmeBaseAdmin):
	fields = ('predicate', 'language', 'label')

class referencesAdmin(DalmeBaseAdmin):
	fields = ('foreign_id', 'type', 'source_id', 'comments')

class repositoryAdmin(DalmeBaseAdmin):
	fields = ('temp')

class reference_attributesAdmin(DalmeBaseAdmin):
    fields = ('subject', 'predicate', 'object')

class repository_attributesAdmin(DalmeBaseAdmin):
    fields = ('subject', 'predicate', 'object')

admin.site.register(external_lemmata, external_lemmataAdmin)
admin.site.register(external_lemma_attributes, external_lemma_attributesAdmin)
admin.site.register(phrases, phrasesAdmin)
admin.site.register(source_attributes, source_attributesAdmin)
admin.site.register(sources, sourcesAdmin)
admin.site.register(superlemmata, superlemmataAdmin)
admin.site.register(superlemma_components, superlemma_componentsAdmin)
admin.site.register(concepts, conceptsAdmin)
admin.site.register(concept_components, concept_componentsAdmin)
admin.site.register(inventories, inventoriesAdmin)
admin.site.register(leaves, leavesAdmin)
admin.site.register(tokens, tokensAdmin)
admin.site.register(inventory_attributes, inventory_attributesAdmin)
admin.site.register(predicates, predicatesAdmin)
admin.site.register(predicate_labels, predicate_labelsAdmin)
admin.site.register(references, referencesAdmin)
admin.site.register(repository, repositoryAdmin)
admin.site.register(reference_attributes, reference_attributesAdmin)
admin.site.register(repository_attributes, repository_attributesAdmin)
