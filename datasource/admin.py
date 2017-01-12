from django.contrib import admin

from datasource.models import DataSource

def datasource_start(modeladmin, request, queryset):
    for obj in queryset:
        obj.action_start()
datasource_start.short_description = "Activate the datasource"


class DataSource_ModelAdmin(admin.ModelAdmin):
    list_display        = ('start_date', 'end_date', 'data_source_type', 'round', 'source_url',)
    list_display_links  = ('data_source_type', )
    list_filter         = ['start_date',]
    list_editable       = ('start_date','end_date',)
    actions = [datasource_start]


admin.site.register(DataSource, DataSource_ModelAdmin)
