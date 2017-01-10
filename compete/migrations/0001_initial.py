# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-12 11:27
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sport', '0007_auto_20161212_1742'),
        ('party', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompetitionRound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('award_points', models.IntegerField(blank=True, choices=[(0, 'no'), (1, 'yes')], null=True)),
                ('competition', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Competition')),
                ('season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sport.Season')),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sport.Venue')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('reg_id', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'ordering': ['reg_id'],
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('time', models.TimeField(blank=True, default=datetime.datetime.now, null=True)),
                ('xpos', models.IntegerField(blank=True, null=True)),
                ('ypos', models.IntegerField(blank=True, null=True)),
                ('zpos', models.IntegerField(blank=True, null=True)),
                ('period', models.IntegerField(blank=True, null=True)),
                ('count', models.IntegerField(default=1)),
                ('entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Entry')),
            ],
            options={
                'ordering': ['period', 'time'],
            },
        ),
        migrations.CreateModel(
            name='EventAttribute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=200)),
                ('entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Entry')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compete.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=100)),
                ('points', models.IntegerField(default=0)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.EventTemplate')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Sport')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fixture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='fixture date')),
                ('category', models.CharField(choices=[('Game', 'Game'), ('Practice', 'Practice'), ('Freindly', 'Freindly')], default='Game', max_length=50)),
                ('subcategory', models.CharField(choices=[('Regular', 'Regular'), ('Semi-Final', 'Semi-Final'), ('Final', 'Final'), ('Play-off', 'Play-off'), ('Exibition', 'Exibition'), ('Quarter-final', 'Quarter-final'), ('Pre-Season', 'Pre-Season')], default='Regular', max_length=50)),
                ('over_times', models.IntegerField(default=0)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='PointsEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('points', models.IntegerField(blank=True, null=True)),
                ('position', models.IntegerField(blank=True, null=True)),
                ('competition', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sport.Competition')),
                ('competition_round', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.CompetitionRound')),
                ('entry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Entry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation time')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('In-Active', 'In-Active'), ('Closed', 'Closed'), ('Tentative', 'Tentative'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')], default='Active', max_length=100)),
                ('priority', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=20)),
                ('default_id', models.CharField(blank=True, max_length=10, null=True)),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Sport')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('organisation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='party.Organisation')),
            ],
            options={
                'abstract': False,
            },
            bases=('party.organisation',),
        ),
        migrations.CreateModel(
            name='IndividualFixture',
            fields=[
                ('fixture_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='compete.Fixture')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='individual_team', to='compete.Team')),
            ],
            options={
                'abstract': False,
            },
            bases=('compete.fixture',),
        ),
        migrations.CreateModel(
            name='TeamFixture',
            fields=[
                ('fixture_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='compete.Fixture')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Team1', to='compete.Team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Team2', to='compete.Team')),
            ],
            options={
                'abstract': False,
            },
            bases=('compete.fixture',),
        ),
        migrations.AddField(
            model_name='pointsentry',
            name='fixture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Fixture'),
        ),
        migrations.AddField(
            model_name='pointsentry',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Team'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='competition',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Competition'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='competition_round',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.CompetitionRound'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='sport',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sport.Sport'),
        ),
        migrations.AddField(
            model_name='fixture',
            name='venue',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fixture_venue', to='sport.Venue'),
        ),
        migrations.AddField(
            model_name='eventattribute',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Team'),
        ),
        migrations.AddField(
            model_name='event',
            name='fixture',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Fixture'),
        ),
        migrations.AddField(
            model_name='event',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Team'),
        ),
        migrations.AddField(
            model_name='event',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compete.EventTemplate'),
        ),
        migrations.AddField(
            model_name='entry',
            name='fixture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compete.Fixture'),
        ),
        migrations.AddField(
            model_name='entry',
            name='people',
            field=models.ManyToManyField(blank=True, related_name='entry_people', to='party.Individual'),
        ),
        migrations.AddField(
            model_name='entry',
            name='person',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='party.Individual'),
        ),
        migrations.AddField(
            model_name='entry',
            name='position',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compete.Position'),
        ),
    ]
