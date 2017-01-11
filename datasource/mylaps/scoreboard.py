import datetime
from django.utils import timezone

from cbe.party.models import Individual
from sport.models import Sport, Venue, Competition
from compete.models import CompetitionRound
from motorsport.models import Race, RaceClass, RaceEntry, Lap, RaceCar


class ScoreboardHandler():
    def __init__(self, datasource, competition, round, date):
        self._parsers = {'$F':self.parse_heartbeat,
                         '$A':self.parse_competitor_information1,
                         '$COMP':self.parse_competitor_information2,
                         '$B':self.parse_run_information,
                         '$C':self.parse_class_information,
                         '$E':self.parse_setting_information,
                         '$G':self.parse_race_information,
                         '$H':self.parse_qualifying_information,
                         '$I':self.parse_init_record,
                         '$J':self.parse_passing_information,
                         '$SP':self.parse_pass,
                         '$SR':self.parse_pass,
                         '$DATE':self.parse_date,
                         '$RND':self.parse_round,
                         }
        self.competition = competition
        self.round = round
        self.date = date
        self.race = None
        self._init_race = False
                         

    def find_entry_car( self, entry, race_class ):
        #Get car. Highest PK means most recently added car so order by pk decending
        cars = RaceCar.objects.filter(car_id_txt=entry.car_id_txt, race_class=race_class).order_by('-pk')
        if len(cars) > 0:
            return cars[0]


    def parse(self,data):
        data = data.split(',')
        
        if data and data[0][0] == '$':
            parse_func = self._parsers[data[0]]
            return parse_func(data)
        else:
            print( "Packet error: Data = %s" %data )
            
            
    def parse_pass(self,data):
        pass
    
    
    def parse_date(self,data):
        """
    0   $DATE
    1   Date              "DD-MM-YYYY"           Current date
        """
        
        date = data[1].strip('"')
        self.date = datetime.date(day=int(date[0:2]),month=int(date[3:5]),year=int(date[6:10]))


    def parse_round(self,data):
        """
        0   $RND
        1   Round Name              'Round 1'
        """

        rnd_name = data[1].strip('"')
        self.round = CompetitionRound.objects.get(competition=self.competition, name=rnd_name)


    def parse_heartbeat(self,data):
        """
        0   $F
        1   Laps to go              0 - 99999           Number of laps to go
        2   Time to go              "HH:MM:SS"          Time until the session ends.
        3   Time of day             "HH:MM:SS"          The current time
        4   Race time               "HH:MM:SS"          The time from the first green flag.
        5   Flag status             "Green "            The status field is 6 characters long with trailing spaces.
                                    "Yellow"
                                    "Red "
                                    "Finish"
        """
        
        if len(data) != 6:
            raise ValueError("Hearbeat format length error:%s"%data)

        race_changes = []
        status = data[5].strip('"').strip(' ')
        laps_to_go = int(data[1])

        if int(data[1]) == 9999:        #TODO: Timed race
            pass

        try:
            self.mylaps_time = datetime.time(int(data[3][1:3]),int(data[3][4:6]),int(data[3][7:9]))
        except:
            self.mylaps_time = datetime.datetime.now().time()

        if data[5] in ('"Green "','"Yellow"'):
            self.racing = True
        else:
            self.racing = False
            
        if self.race is None:
            print( "No race to apply data to - waiting for run info or command from gfx control" )
        else:
            if self.race.status != 'Finish':
                # Has race status changed
                if self.race.status != status:
                    self.race.status = status
                    race_changes.append("status")

                # Has laps to go changed
                if laps_to_go < 900 and self.race.laps_to_go != laps_to_go:
                    self.race.laps_to_go = laps_to_go
                    race_changes.append("laps to go")

                # If race status has changed to finished then set finish time
                if self.race.status == 'Finish':
                    self.race.finish_time = timezone.make_aware(datetime.datetime.combine(self.date,self.mylaps_time), timezone.get_current_timezone())
                    self.race.current_lap_number = self.race.total_laps
                    race_changes.append("finished")
                    
                elif laps_to_go < 900:
                    if self.race.total_laps == 0 or self.race.total_laps == None:
                        self.race.total_laps = laps_to_go
                        race_changes.append("total laps")
                    self.race.current_lap_number = (self.race.total_laps - self.race.laps_to_go)+1

            if self.racing == True:
                if data[4]=='"00:00:00"':
                    self.race.total_laps=int(data[1])
                    race_changes.append("race start laps")

                if self.race.start_time == None:
                    self.race.start_time = timezone.make_aware(datetime.datetime.combine(self.date,self.mylaps_time), timezone.get_current_timezone())
                    race_changes.append("race start time")
                    
            minstogo = int(data[2][4:6])
            secstogo = (minstogo*60)+int(data[2][7:9])

            if self.race.time_to_go is None or self.race.time_to_go != datetime.timedelta(microseconds=minstogo*10000*100*60):
                self.race.time_to_go = datetime.timedelta(microseconds=minstogo*10000*100*60)
                race_changes.append("time to go")

        if race_changes != []:
            self.race.save()
        return race_changes


    def parse_competitor_information1(self,data):
        """
        0   $A
        1   Registration number     characters          8 characters maximum (this is usually the competitor number).
        2   Number                  characters          5 characters maximum.
        3   Transponder number      1 - .097.151
        4   First name              characters          9 characters maximum.
        5   Last name               characters          30 characters maximum.
        6   Nationality             characters          50 characters maximum.
        7   Class number            1 - 99              The unique class number.
        """
    
        if len(data) != 8:
            if len(data) == 9:
                data[7] = data[8]
            else:
                raise ValueError("Malformed competitor information, ignoring: %s" %data)

        # Don't accept competitor information for a finished race
        if self.race:
            if self.race.status == 'Finish':
                return
        
        full_first_name = "%s"%(data[4].strip('"').strip())
        full_last_name=data[5].strip('"').strip()

        current_driver = None
        if full_first_name.find('#') != -1:
            current_driver = 0
        if full_last_name.find('#') != -1:
            current_driver = 1
        
        reg_no = data[1].strip('"').strip()
        car_id_txt=data[2].strip('"').strip()
        first_name=data[4].strip('"').strip().strip('#').strip()
        last_name=data[5].strip('"').strip().strip('#').strip()
        nationality=data[6].strip('"').strip()

        # If first name contains the whole thing and last name is empty then split up
        if len(last_name) == 0:
            name_split = first_name.split(' ')
            first_name = name_split[0]
            last_name = " ".join(name_split[1:])

        if reg_no == "SC":
            print( "Safety car info, ignored" )
            return

        if len( first_name ) == 0:
            print( "Empty first name. Not processing $A" )
            return

        if reg_no in self.entries:
            entry = self.entries[reg_no]
            print( "Found existing entry: %s" %entry )
            

            driver = entry.driver
            print( "ENTRY FOUND WITH DRIVER:%s"%driver )
            if driver.first_name != first_name or driver.last_name != last_name:
                print( "Entry not matched with driver. Adding new driver: %s %s" %(first_name,last_name) )
                driver = Individual.objects.filter(first_name=first_name, last_name=last_name)
                if len(driver) > 0:
                    driver = driver[0]
                else:
                    driver = Individual(first_name=first_name, last_name=last_name)
                    driver.save()

                race_classes = RaceClass.objects.filter(race=self.race)
                if len(race_classes) > 0:
                    entry.car=self.find_entry_car(entry, race_classes[0])
                    entry.race_class = race_classes[0]

                entry.timing_id = data[7]
                entry.save()

        elif self.race:
            print( "$A no entry for: %s -> name = %s %s, number = %s - adding"%(reg_no,first_name,last_name,data[2]) )
            driver = Individual.objects.filter(first_name=first_name, last_name=last_name)
            if len(driver) > 0:
                driver = driver[0]
            else:
                driver = Individual(first_name=first_name, last_name=last_name)
                driver.save()

            entry = RaceEntry(reg_id=reg_no, race=self.race, car_id_txt=car_id_txt, driver=driver)

            race_classes = RaceClass.objects.filter(race=self.race)
            if len(race_classes) > 0:
                entry.car=self.find_entry_car(entry, race_classes[0])
                entry.race_class = race_classes[0]

            entry.timing_id = data[7]
            entry.save()
            self.entries[reg_no] = entry
        else:
            print( "NO RACE TO ADD ENTRY" )
                
                
    def parse_competitor_information2(self,data):
        """
        0   $COMP
        1   Registration number     characters          8 characters maximum (this is usually the competitor number).
        2   Number                  characters          5 characters maximum.
        3   Class number            1 - 99              The unique class number.
        4   First name              characters          9 characters maximum.
        5   Last name               characters          30 characters maximum.
        6   Nationality             characters          50 characters maximum.
        7   Additional data         characters          50 characters maximum.
        """

        reg_id = reg_no = data[1].strip('"').strip()
        if reg_id == "SC":
            print( "Safety car info, ignored" )
            return
        if reg_no in self.entries:
            entry = self.entries[reg_no]
        else:
            print( "$COMP no entry for: %s -> name = %s %s, number = %s"%(reg_id,data[4],data[5],data[2]) )


    def parse_run_information(self,data):
        """
        0   $B
        1   Unique number           1 - 99              A unique run number.
        2   Description             characters          40 characters maximum.
        """

        changed = False
        race = Race.objects.filter(number=data[1],competition_round=self.current_round)
        
        race_name = data[2].strip('"')
        race_number = int(data[1])
        
        if len(race)>0:
            race = race[0]
            if race != self.race and race_name != self.race.name:
                self.race = race
                self.entries = {}
                for entry in RaceEntry.objects.filter(race=self.race):
                    if self._init_race == True:
                        entry.delete()
                        changed = True
                    else:
                        self.entries[entry.reg_id] = entry                        
            if self._init_race == True and self.race.status != 'Finish':
                self._init_race = False
                Lap.objects.filter(race=self.race).delete()
                self.race.race_classes.clear()
        else:
            self.race = Race(sport=self.sport, competition=self.current_round.competition, venue=self.current_round.venue, competition_round=self.current_round,name=race_name, number=race_number,total_laps=0,current_lap=0, award_points = 1, qualification=qualification)
            self.race.save()
            self.entries = {}
            self._init_race = False

           
            
    def parse_class_information(self,data):
        """
        0   $C
        1   Unique number           1 - 99              A unique (for current race) class number.
        2   Description             characters          40 characters maximum.
        """

        
        if self.race:
            if self.race.status == 'Finish':
                return
                
        class_name = data[2].strip('"')

        if self.race:
            race_class, created = RaceClass.objects.get_or_create(name=class_name)
            race_classes = self.race.race_classes.filter(name=race_class.name)
            
            if len(race_classes) == 0:
                print( "Adding race class %s to race %s"%(race_class,self.race) )
                self.race.race_classes.add(race_class)
                self.race.save()

                
    def parse_setting_information(self,data):
        """
        0   $E
        1   Description             Name of the setting TRACKNAME
                                                        TRACKLENGTH
        2   Value                   characters          40 characters maximum.
        """
        
        pass


    def parse_race_information(self,data):
        """
        0   $G
        1   Position                1 - 999             The race position.
        2   Registration number     characters          8 characters maximum.
        3   Laps                    0 -99999           The lap number
        4   Total time            "HH:MM:SS.DDD"      The total time
        """

        pass


    def parse_qualifying_information(self,data):
        """
        0   $H
        1   Position                1 - 999             The practice/qualifying position.
        2   Registration number     characters          8 characters maximum.
        3   Best lap                0 - 99999           The lap number of the best lap
        4   Best laptime            "HH:MM:SS.DDD"      The laptime of the best lap.
        """

        pass
            
            
    def parse_init_record(self,data):
        """
        0   $I
        1   Time of day             "HH:MM:SS.DDD"      Current time
        2   Date                    "dd mmm yy"         Current date
        """

        self._init_race = True
    
    
    def parse_passing_information(self,data):
        """
        0   $J
        1   Registration number     characters          8 characters maximum.
        2   Laptime                 "HH:MM:SS.DDD"      The current lap time
        3   Total time              "HH:MM:SS.DDD"      The total time.
        """

        pass


    def parse_sector_information(self,data):
        """
        0   $J
        1   Registration number     characters          8 characters maximum.
        2   Laptime                 "HH:MM:SS.DDD"      The current lap time
        3   Total time              "HH:MM:SS.DDD"      The total time.
        """

        pass