from django.contrib import admin

from .models import SiteResources


class SiteResourceAdmin(admin.ModelAdmin):
    filter_horizontal = ('resources',)
    readonly_fields = ('site',)

admin.site.register(SiteResources, SiteResourceAdmin)
