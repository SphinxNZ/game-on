import datetime, time
from django.db import models

from cbe.party.models import Individual, Organisation
from cbe.physical_object.models import Vehicle

from sport.models import Sport
from compete.models import CompetitionRound, Entry, Fixture, Event


class AmericanFootballEvent(Event):
    pass

class BaseballEvent(Event):
    pass

class BasketballEvent(Event):
    pass

class BowlsEvent(Event):
    pass

class CricketEvent(Event):
    pass
    
class CueEvent(Event):
    pass

class DodgeballEvent(Event):
    pass

class FootballEvent(Event):
    pass

class RugbyLeagueEvent(Event):
    pass

class RugbyUnionEvent(Event):
    pass

class GolfEvent(Event):
    pass

class HandballEvent(Event):
    pass

class HurlingEvent(Event):
    pass

class LacrosseEvent(Event):
    pass

class NetballEvent(Event):
    pass

class PoloEvent(Event):
    pass

class SquashEvent(Event):
    pass

class VolleyballEvent(Event):
    pass
    