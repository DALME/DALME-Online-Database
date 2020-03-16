from django.contrib import admin

from solo.admin import SingletonModelAdmin

from dalme_public.models import Collection, HomePage, Set


admin.site.register(HomePage, SingletonModelAdmin)
admin.site.register(Collection)
admin.site.register(Set)
