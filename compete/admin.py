from django.contrib import admin

from cbe.party.models import Individual, Organisation
from sport.models import Competition
from compete.models import Team, TeamFixture,IndividualFixture, Fixture, Entry
from compete.models import EventTemplate, Event, EventAttribute, PointsEntry
from compete.models import Position, CompetitionRound


class EventAttribute_InLine(admin.TabularInline):
    model = EventAttribute
    extra = 1
    

class Event_InLine(admin.TabularInline):
    model = Event
    extra = 1

    
class Entry_InLine(admin.TabularInline):
    model = Entry
    extra = 1    

    
class EventTemplate_ModelAdmin(admin.ModelAdmin):
    list_display        = ('sport','parent','name','points','priority')
    list_display_links  = ('name',)
    list_filter         = ['sport','name','parent',]

    
class Event_ModelAdmin(admin.ModelAdmin):
    list_display        = ('created','fixture','event_type','start_time','finish_time','duration', 'template','entry')
    list_display_links  = ('created','event_type','start_time')
    list_filter         = ['event_type','template']
    inlines = [EventAttribute_InLine,]


class PointsEntry_ModelAdmin(admin.ModelAdmin):
    list_display        = ('competition','competition_round','points','entry','team','fixture',)
    list_display_links  = ('fixture',)
    list_filter         = ['fixture',]

    
class Position_ModelAdmin(admin.ModelAdmin):
    list_display        = ('sport','name','default_id',)
    list_display_links  = ('name',)
    list_filter         = ['name',]


class Fixture_ModelAdmin(admin.ModelAdmin):
    valid_lookups = ('competition', 'sport')
    list_display        = ('date','fixture_type','sport','competition','competition_round','venue',)
    list_display_links  = ('date',)
    list_filter         = ['fixture_type','date','sport','competition','venue']
    inlines = [Entry_InLine, Event_InLine,]    

    
class TeamFixture_ModelAdmin(admin.ModelAdmin):
    valid_lookups = ('competition', 'sport')
    list_display        = ('date','sport','competition', 'competition_round', 'category', 'subcategory', )
    list_display_links  = ('date',)
    list_filter         = ['date','sport','subcategory','competition','venue']
    list_per_page = 50
   

class IndividualFixture_ModelAdmin(admin.ModelAdmin):
    list_display        = ('date','competition','competition_round','venue','category','subcategory')
    list_display_links  = ('date',)
    list_filter         = ['date','competition','venue','category']
    inlines = [Entry_InLine, Event_InLine,]    


class CompetitionRound_ModelAdmin(admin.ModelAdmin):
    valid_lookups = ('competition', 'sport')
    list_display        = ('start_date', 'end_date', 'competition', 'season', 'priority','venue', 'name',)
    list_display_links  = ('venue', )
    list_filter         = ['competition','venue']
    list_editable       = ('start_date','name','season','priority','start_date', 'end_date',)


admin.site.register(Team)
admin.site.register(Entry)
admin.site.register(Fixture, Fixture_ModelAdmin)
admin.site.register(TeamFixture, TeamFixture_ModelAdmin)
admin.site.register(IndividualFixture, IndividualFixture_ModelAdmin)
admin.site.register(CompetitionRound, CompetitionRound_ModelAdmin)
admin.site.register(Event,Event_ModelAdmin)
admin.site.register(PointsEntry,PointsEntry_ModelAdmin)
admin.site.register(EventTemplate,EventTemplate_ModelAdmin)
admin.site.register(Position,Position_ModelAdmin)
