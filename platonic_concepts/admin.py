from django.contrib import admin

from .models import PlatonicConcept, Relationship

class PlatonicConceptAdmin(admin.ModelAdmin):
    fields = ('term','comments')
    def save_model(self, request, obj, form, change):
        if not change:
            obj.creation_username = request.user.username
        obj.modification_username = request.user.username
        obj.save()

admin.site.register(PlatonicConcept, PlatonicConceptAdmin)
admin.site.register(Relationship)
