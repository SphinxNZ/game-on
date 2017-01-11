from django.db import models
from django.contrib.auth.models import User, Group

from cbe.location.models import UrbanPropertyAddress, City, Country
from cbe.party.models import Organisation

class Base(models.Model):
    created = models.DateTimeField('creation time',auto_now_add=True)
    modified = models.DateTimeField('modified time',auto_now=True)
    status = models.CharField(max_length=100, choices=( ('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled'), ), default='Active')
    priority = models.IntegerField(default=0)

    class Meta:
        abstract = True


class Sport(Base):
    name = models.CharField(max_length=200)

    def __str__(self):
        return '%s'%self.name

        
class Venue(Base):
    real_name = models.CharField(max_length=100)
    sponsored_name = models.CharField(max_length=100)
    location = models.ForeignKey(UrbanPropertyAddress, blank=True, null=True)
    sports = models.ManyToManyField(Sport, blank=True)
    sponsor = models.ForeignKey(Organisation, blank=True, null=True)

    @property
    def name(self):
        if self.real_name != self.sponsored_name:
            return self.sponsored_name
        return self.real_name

    def __str__(self):
        return '%s, %s'%(self.name, self.location)


class CompetitionLevel(Base):
    name = models.CharField(max_length = 100)
    parent = models.ForeignKey('CompetitionLevel',null=True,blank=True)

    class Meta:
        ordering = ['parent__id','name']        

    def __str__(self):
        return u'%s' % (self.name)


class Competition(Base):
    parent = models.ForeignKey('Competition',null=True,blank=True)
    sport = models.ForeignKey(Sport)
    competition_level = models.ForeignKey(CompetitionLevel,null=True,blank=True)

    name = models.CharField(max_length=100)
    cities = models.ManyToManyField(City, blank=True)
    countries = models.ManyToManyField(Country, blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    
    def __str__(self):
        return '%s'%(self.name)

    class Meta:
        ordering = ['parent__id','name']        


class Season(Base):
    competition = models.ForeignKey(Competition)
    name = models.CharField(max_length=100)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    sponsor = models.ForeignKey(Organisation, blank=True, null=True)

    def __unicode__(self):
        return unicode(u'%s' % (self.name))
    
