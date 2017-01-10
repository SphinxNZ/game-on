from django.contrib import admin

from sport.models import Sport, Venue, Competition, CompetitionLevel, Season
from compete.models import CompetitionRound

class Competition_InLine(admin.TabularInline):
    model = Competition
    extra = 0

    
class CompetitionRound_InLine(admin.TabularInline):
    model = CompetitionRound
    extra = 0

    
class CompetitionLevel_ModelAdmin(admin.ModelAdmin):
    list_display        = ('name','parent',)
    list_display_links  = ('name',)
    list_filter         = ['name',]

    
class Competition_ModelAdmin(admin.ModelAdmin):
    list_display        = ('sport', 'name','status','start_date','end_date',)
    list_display_links  = ('name',)
    list_filter         = ('sport','status')
    inlines = [CompetitionRound_InLine,]

    
class Sport_ModelAdmin(admin.ModelAdmin):
    list_display        = ('name','status')
    list_display_links  = ('name',)
    inlines = [Competition_InLine,]

    
class Venue_ModelAdmin(admin.ModelAdmin):
    list_display        = ('name',)
    list_display_links  = ('name',)

    
class Season_ModelAdmin(admin.ModelAdmin):
    list_display        = ('competition', 'name','start_date','end_date',)
    list_display_links  = ('name',)
    list_filter         = ['competition', ]
    inlines = [CompetitionRound_InLine,]

    
admin.site.register(CompetitionLevel,CompetitionLevel_ModelAdmin)
admin.site.register(Competition,Competition_ModelAdmin)
admin.site.register(Sport,Sport_ModelAdmin)
admin.site.register(Venue,Venue_ModelAdmin)
admin.site.register(Season,Season_ModelAdmin)