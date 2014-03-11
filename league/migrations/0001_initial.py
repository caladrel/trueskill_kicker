# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table(u'league_player', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mu', self.gf('django.db.models.fields.FloatField')(default=25.0)),
            ('sigma', self.gf('django.db.models.fields.FloatField')(default=8.333333333333334)),
            ('rank', self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True)),
        ))
        db.send_create_signal(u'league', ['Player'])

        # Adding model 'Match'
        db.create_table(u'league_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score_team1', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('score_team2', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('team1_player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['league.Player'])),
            ('team1_player2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['league.Player'])),
            ('team2_player1', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['league.Player'])),
            ('team2_player2', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['league.Player'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
        ))
        db.send_create_signal(u'league', ['Match'])


    def backwards(self, orm):
        # Deleting model 'Player'
        db.delete_table(u'league_player')

        # Deleting model 'Match'
        db.delete_table(u'league_match')


    models = {
        u'league.match': {
            'Meta': {'object_name': 'Match'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score_team1': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'score_team2': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'team1_player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['league.Player']"}),
            'team1_player2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['league.Player']"}),
            'team2_player1': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['league.Player']"}),
            'team2_player2': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['league.Player']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'})
        },
        u'league.player': {
            'Meta': {'object_name': 'Player'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mu': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'rank': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'sigma': ('django.db.models.fields.FloatField', [], {'default': '8.333333333333334'})
        }
    }

    complete_apps = ['league']