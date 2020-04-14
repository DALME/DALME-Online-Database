from django.contrib import admin

from solo.admin import SingletonModelAdmin

from dalme_app.models import Set as DALMESet
from dalme_public.models import Collection, HomePage, Set


class CollectionAdmin(admin.ModelAdmin):
    exclude = ('set_type',)

    def render_change_form(self, request, context, *args, **kwargs):
        qs = DALMESet.objects.filter(set_type=Collection.set_type)
        context['adminform'].form.fields['source_set'].queryset = qs
        return super().render_change_form(request, context, *args, **kwargs)


class SetAdmin(admin.ModelAdmin):
    exclude = ('set_type',)

    def render_change_form(self, request, context, *args, **kwargs):
        qs = DALMESet.objects.filter(set_type=Set.set_type)
        context['adminform'].form.fields['source_set'].queryset = qs
        return super().render_change_form(request, context, *args, **kwargs)


admin.site.register(HomePage, SingletonModelAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Set, SetAdmin)
