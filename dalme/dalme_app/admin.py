from django.contrib import admin
from .models import par_inventories, par_folios, par_tokens, error_messages, par_objects

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
