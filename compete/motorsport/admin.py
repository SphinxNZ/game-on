from django.contrib import admin

from compete.motorsport.models import Race, RaceClass, RaceCar, RaceEntry
from compete.motorsport.models import Lap

class RaceEntry_InLine(admin.TabularInline):
    model = RaceEntry
    extra = 1

class Race_InLine(admin.TabularInline):
    model = Race
    extra = 1

class Lap_InLine(admin.TabularInline):
    model = Lap
    extra = 1

class RaceEntry_ModelAdmin(admin.ModelAdmin):
    list_display        = ('fixture', 'race_class', 'car_id_txt', 'car', 'person','grid_pos','current_lap','current_position' )
    list_display_links  = ('car_id_txt', 'car', 'person',)
    list_filter         = ['fixture__competition_round', 'race_class', 'person', ]
    

class Race_ModelAdmin(admin.ModelAdmin):
    list_display        = ('pk','number', 'name', 'competition_round','status','total_laps',)
    list_display_links  = ('pk','name',)
    list_filter         = ['competition_round']
    list_editable       = ('status',)
    inlines = [RaceEntry_InLine,]

class RaceClass_ModelAdmin(admin.ModelAdmin):
    list_display        = ('name',)
    list_display_links  = ('name',)
    list_filter         = ['name',]

class RaceCar_ModelAdmin(admin.ModelAdmin):
    list_display        = ('race_class','car_id_txt','sponsor','make','series','model','tyres',)
    list_display_links  = ('car_id_txt',)
    list_editable    = ('sponsor','make','tyres', )
    list_filter         = ['race_class','make']

class Lap_ModelAdmin(admin.ModelAdmin):
    list_display        = ('fixture','lap_number','entry','start_time','finish_time','duration',)
    list_display_links  = ('lap_number','entry',)
    list_filter         = ['fixture','entry',]

admin.site.register(RaceCar,RaceCar_ModelAdmin)
admin.site.register(Race,Race_ModelAdmin)
admin.site.register(RaceClass,RaceClass_ModelAdmin)
admin.site.register(Lap,Lap_ModelAdmin)
admin.site.register(RaceEntry,RaceEntry_ModelAdmin)    