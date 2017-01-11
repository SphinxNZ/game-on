from django.contrib import admin

from compete.ballsport.models import AmericanFootballEvent, BaseballEvent, BasketballEvent, BowlsEvent
from compete.ballsport.models import CricketEvent, CueEvent, DodgeballEvent, FootballEvent
from compete.ballsport.models import RugbyLeagueEvent, RugbyUnionEvent, GolfEvent, HurlingEvent
from compete.ballsport.models import LacrosseEvent, NetballEvent, PoloEvent, SquashEvent, VolleyballEvent

class Event_ModelAdmin(admin.ModelAdmin):
    list_display        = ('fixture', 'template', 'entry', 'start_time', 'finish_time','duration','xpos','ypos','zpos', )
    list_display_links  = ('fixture', 'template', 'entry', 'start_time', 'finish_time','duration',)
    list_filter         = ['template', 'start_time']
    
admin.site.register(AmericanFootballEvent,Event_ModelAdmin)
admin.site.register(BaseballEvent,Event_ModelAdmin)
admin.site.register(BasketballEvent,Event_ModelAdmin)
admin.site.register(BowlsEvent,Event_ModelAdmin)
admin.site.register(CricketEvent,Event_ModelAdmin)
admin.site.register(CueEvent,Event_ModelAdmin)
admin.site.register(DodgeballEvent,Event_ModelAdmin)
admin.site.register(FootballEvent,Event_ModelAdmin)
admin.site.register(RugbyLeagueEvent,Event_ModelAdmin)
admin.site.register(RugbyUnionEvent,Event_ModelAdmin)
admin.site.register(GolfEvent,Event_ModelAdmin)
admin.site.register(HurlingEvent,Event_ModelAdmin)
admin.site.register(LacrosseEvent,Event_ModelAdmin)
admin.site.register(NetballEvent,Event_ModelAdmin)
admin.site.register(PoloEvent,Event_ModelAdmin)
admin.site.register(SquashEvent,Event_ModelAdmin)
admin.site.register(VolleyballEvent,Event_ModelAdmin)
