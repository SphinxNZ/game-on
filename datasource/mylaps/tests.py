import datetime

from django.utils import timezone
from django.test import TestCase

from sport.models import Sport, Competition, Venue
from compete.models import CompetitionRound
from compete.motorsport.models import Race

from datasource.models import DataSource
from datasource.mylaps.scoreboard import ScoreboardHandler

class ScoreboardTestCase(TestCase):

    def setUp(self):
        sport = Sport.objects.create(name="test sport")
        competition = Competition.objects.create(sport=sport, name="test comp")
        round = CompetitionRound.objects.create(competition=competition, name="test round")
        venue = Venue.objects.create(real_name="test venue")
        datasource = DataSource.objects.create(data_source_type="Client", round=round )
        race = Race.objects.create( sport=sport, competition=competition, venue=venue, number=1, name="test race" )

        self.handler = ScoreboardHandler(datasource, competition, round, timezone.datetime.now().date())
        self.handler.race = race
        

    def test_heartbeat(self):
        """
        Make sure the heartbeat works
        """
        changes = self.handler.parse('$F,14,"00:12:45","13:34:23","00:09:47","Green "')
        self.assertEqual(self.handler.race.status,"Green")
        changes = self.handler.parse('$F,14,"00:12:45","13:34:22","00:09:47","Green "')
        self.assertEqual(changes,[])
        changes = self.handler.parse('$F,14,"00:11:45","13:34:22","00:09:47","Green "')
        self.assertEqual(changes,["time to go",])
        changes = self.handler.parse('$F,0,"00:00:00","13:34:23","00:09:47","Finish"')
        self.assertTrue("status" in changes)
        self.assertTrue("finished" in changes)
        self.assertTrue("time to go" in changes)
        