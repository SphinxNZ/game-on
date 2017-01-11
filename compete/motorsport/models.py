import datetime, time
from django.db import models

from cbe.party.models import Individual, Organisation
from cbe.physical_object.models import Vehicle

from sport.models import Sport
from compete.models import CompetitionRound, Entry, Fixture, Event


class RaceClass(models.Model):
    name = models.CharField(max_length=50)
    sponsor = models.CharField(max_length=100,null=True, blank=True)
    
    def __str__(self):
        return self.name


class Race(Fixture):
    race_classes = models.ManyToManyField(RaceClass,blank=True)

    method = models.CharField(max_length=100, choices=( ('laps', 'laps'), ('duration', 'duration'), ('duration', 'laps or duration'), ),default='laps')

    total_laps = models.IntegerField(null=True, blank=True)
    total_duration = models.DurationField(null=True,blank=True)

    current_lap_number = models.IntegerField(null=True, blank=True)
    laps_to_go = models.IntegerField(null=True, blank=True)
    time_to_go = models.DurationField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.fixture_type is None or self.fixture_type == "":
            self.fixture_type = "Race"          
        super(Race, self).save(*args, **kwargs)
    
    
class Lap(Event):
    lap_number = models.IntegerField()
    position = models.IntegerField(null=True,blank=True)

    gap = models.DurationField(null=True,blank=True)
    race_time = models.DurationField(null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.event_type is None or self.event_type == "":
            self.event_type = "Lap"          
        super(Lap, self).save(*args, **kwargs)
        
    
class RaceCar(Vehicle):
    car_id_txt = models.CharField(max_length=10)
    sponsor = models.CharField(max_length=200,blank=True)
    tyres = models.CharField(max_length=100,blank=True)
    colours = models.CharField(max_length=100,blank=True)

    race_class = models.ForeignKey('RaceClass',null=True,blank=True)
    
    
class RaceEntry(Entry):
    timing_id = models.IntegerField(null=True,blank=True)
    race_class = models.ForeignKey(RaceClass,null=True,blank=True)

    car_id_txt = models.CharField(max_length=10,null=True,blank=True)
    codriver = models.ForeignKey(Individual,related_name="codriver",null=True,blank=True)
    car = models.ForeignKey(RaceCar,null=True,blank=True)

    grid_pos = models.IntegerField(null=True,blank=True)
    start_time = models.TimeField(null=True,blank=True)
    finish_pos = models.IntegerField(null=True,blank=True)
    finish_time = models.TimeField(null=True,blank=True)

    current_driver = models.IntegerField(default=0)
    current_position = models.IntegerField(null=True,blank=True)
    current_points = models.IntegerField(null=True,blank=True)
    current_gap = models.DurationField(null=True,blank=True)
    current_time = models.DurationField(null=True,blank=True)
    
    current_lap = models.ForeignKey(Lap,related_name="race_entry_current_lap", null=True,blank=True)
    last_lap = models.ForeignKey(Lap,related_name="race_entry_last_lap", null=True,blank=True)
    best_lap = models.ForeignKey(Lap,related_name="race_entry_best_lap", null=True,blank=True)
    