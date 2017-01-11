from django.contrib import admin

from datasource.models import DataSource


class DataSource_ModelAdmin(admin.ModelAdmin):
    list_display        = ('start_date', 'end_date', 'data_source_type', 'round', 'source_url',)
    list_display_links  = ('data_source_type', )
    list_filter         = ['start_date',]
    list_editable       = ('start_date','end_date',)


admin.site.register(DataSource, DataSource_ModelAdmin)
