from datetime import datetime
from django.db import models
from django.utils import timezone

from sport.models import Base, Sport, Venue, Competition, Season
from cbe.party.models import Individual, Organisation


class Team(Organisation):
    sport = models.ForeignKey(Sport)
    competition = models.ForeignKey(Competition)
    
    def save(self, *args, **kwargs):
        if self.organisation_type is None or self.organisation_type == "":
            self.organisation_type = "Team"          
        super(Team, self).save(*args, **kwargs)
        

class CompetitionRound(Base):
    competition = models.ForeignKey(Competition)
    season = models.ForeignKey(Season,null=True,blank=True)

    name = models.CharField(max_length=100)
    venue = models.ForeignKey(Venue,null=True,blank=True)

    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "%s"%self.name


class Fixture(Base):
    sport = models.ForeignKey(Sport)
    competition = models.ForeignKey(Competition)
    competition_round = models.ForeignKey(CompetitionRound, blank=True,null=True)
    fixture_type = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)

    status = models.CharField(max_length=100, null=True,blank=True,)
    venue = models.ForeignKey(Venue, related_name="fixture_venue")
    date = models.DateTimeField('fixture date', default=timezone.now)
    start_time = models.DateTimeField(null=True,blank=True)
    finish_time = models.DateTimeField(null=True,blank=True)

    choices_category = ( ('Competition', 'Competition'), ('Qualification', 'Qualification'), ('Practice', 'Practice'), ('Freindly', 'Freindly'), )
    category = models.CharField(max_length=50, choices=choices_category,default='Competition')

    choices_subcategory = ( ('Regular', 'Regular'), ('Semi-Final', 'Semi-Final'), ('Final', 'Final'), ('Play-off', 'Play-off'), ('Exibition', 'Exibition'), ('Quarter-final', 'Quarter-final'), ('Pre-Season', 'Pre-Season'), )
    subcategory = models.CharField(max_length=50, choices=choices_subcategory,default='Regular')
 
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '%s @ %s: %s' % (self.date, self.venue.name, self.sport)

        
class IndividualFixture(Fixture):

    def __str__(self):
        return '%s @ %s: %s'%(self.date, self.venue, self.sport)

    def save(self, *args, **kwargs):
        if self.fixture_type is None or self.fixture_type == "":
            self.fixture_type = "IndividualFixture"          
        super(IndividualFixture, self).save(*args, **kwargs)

        
class TeamFixture(Fixture):
    team1 = models.ForeignKey(Team, related_name="Team1")
    team2 = models.ForeignKey(Team, related_name="Team2")

    def __str__(self):
        return "%s vs %s"%(self.team1.name,self.team2.name)

    def save(self, *args, **kwargs):
        if self.fixture_type is None or self.fixture_type == "":
            self.fixture_type = "TeamFixture"          
        super(TeamFixture, self).save(*args, **kwargs)
        

class Position(Base):
    sport = models.ForeignKey(Sport)

    name = models.CharField(max_length=20)
    default_id = models.CharField(max_length=10, blank=True,null=True)

    def __str__(self):
        return '%s: %s'%(self.sport, self.name)


class Entry(Base):
    fixture = models.ForeignKey(Fixture)
    position = models.ForeignKey(Position, blank=True,null=True)
    person = models.ForeignKey(Individual, blank=True,null=True)
    team = models.ForeignKey(Team, blank=True,null=True)
    reg_id = models.CharField(max_length=50, blank=True,null=True)

    class Meta:
        ordering = ['fixture','reg_id']        

    def __str__(self):
        return '%s' % (self.reg_id)



class EventTemplate(Base):
    parent = models.ForeignKey('EventTemplate',null=True,blank=True)
    name = models.CharField(max_length=100)
    points = models.IntegerField(default=0)
    sport = models.ForeignKey(Sport)

    def __str__(self):
        return "%s" % self.name


class Event(Base):
    fixture = models.ForeignKey(Fixture)
    parent = models.ForeignKey('Event',null=True,blank=True)
    event_type = models.CharField(max_length=100, blank=True)
    template = models.ForeignKey(EventTemplate,null=True,blank=True)

    entry = models.ForeignKey(Entry, blank=True,null=True)

    start_time = models.TimeField(null=True,blank=True)
    finish_time = models.TimeField(null=True,blank=True)
    duration = models.DurationField(null=True,blank=True)

    xpos = models.IntegerField(blank=True,null=True)
    ypos = models.IntegerField(blank=True,null=True)
    zpos = models.IntegerField(blank=True,null=True)
    count = models.IntegerField(default=1)

    class Meta:
        ordering = ['fixture','created']        


    def __str__(self):
        return "%s - %s: %s by %s" %( self.fixture, self.created, self.template, self.entry )

            

class EventAttribute(models.Model):
    event = models.ForeignKey(Event)
    team = models.ForeignKey(Team, blank=True,null=True)
    entry = models.ForeignKey(Entry, blank=True,null=True)

    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return "%s" % self.name


class PointsEntry(Base):
    entry = models.ForeignKey(Entry, blank=True,null=True)
    team = models.ForeignKey(Team,null=True,blank=True)
    competition_round = models.ForeignKey(CompetitionRound,null=True,blank=True)
    competition = models.ForeignKey(Competition,null=True,blank=True)
    fixture = models.ForeignKey(Fixture,null=True,blank=True)

    points = models.IntegerField(null=True,blank=True)
    position = models.IntegerField(null=True,blank=True)        