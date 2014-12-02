# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score_team1', models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], validators=[django.core.validators.MaxValueValidator(10)])),
                ('score_team2', models.PositiveSmallIntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10)], validators=[django.core.validators.MaxValueValidator(10)])),
                ('timestamp', models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                'verbose_name_plural': 'matches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, db_index=True)),
                ('mu', models.FloatField(default=25.0)),
                ('sigma', models.FloatField(default=8.333333333333334)),
                ('rank', models.FloatField(default=0.0, db_index=True)),
                ('attacker_mu', models.FloatField(default=25.0)),
                ('attacker_sigma', models.FloatField(default=8.333333333333334)),
                ('attacker_rank', models.FloatField(default=0.0, db_index=True)),
                ('defender_mu', models.FloatField(default=25.0)),
                ('defender_sigma', models.FloatField(default=8.333333333333334)),
                ('defender_rank', models.FloatField(default=0.0, db_index=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlayerHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mu', models.FloatField(default=25.0)),
                ('sigma', models.FloatField(default=8.333333333333334)),
                ('rank', models.FloatField(default=0.0)),
                ('was_attacker', models.BooleanField(default=False)),
                ('seperate_mu', models.FloatField(default=25.0)),
                ('seperate_sigma', models.FloatField(default=8.333333333333334)),
                ('seperate_rank', models.FloatField(default=0.0)),
                ('match', models.ForeignKey(to='league.Match')),
                ('player', models.ForeignKey(to='league.Player')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='match',
            name='team1_player1',
            field=models.ForeignKey(related_name='+', to='league.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='team1_player2',
            field=models.ForeignKey(related_name='+', to='league.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='team2_player1',
            field=models.ForeignKey(related_name='+', to='league.Player'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='match',
            name='team2_player2',
            field=models.ForeignKey(related_name='+', to='league.Player'),
            preserve_default=True,
        ),
    ]
