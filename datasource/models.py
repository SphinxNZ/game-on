from django.db import models

from compete.models import CompetitionRound

DATA_SOURCE_CHOICES = (('Server', 'Server'),
                  ('Client', 'Client'), )

                  
class DataSource(models.Model):
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    data_source_type = models.CharField(max_length=100,choices=DATA_SOURCE_CHOICES)

    round = models.ForeignKey(CompetitionRound, null=True,blank=True)
    source_url = models.URLField(null=True,blank=True)
    
        