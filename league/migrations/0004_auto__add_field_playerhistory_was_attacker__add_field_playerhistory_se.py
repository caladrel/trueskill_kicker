# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'PlayerHistory.was_attacker'
        db.add_column(u'league_playerhistory', 'was_attacker',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'PlayerHistory.seperate_mu'
        db.add_column(u'league_playerhistory', 'seperate_mu',
                      self.gf('django.db.models.fields.FloatField')(default=25.0),
                      keep_default=False)

        # Adding field 'PlayerHistory.seperate_sigma'
        db.add_column(u'league_playerhistory', 'seperate_sigma',
                      self.gf('django.db.models.fields.FloatField')(default=8.333333333333334),
                      keep_default=False)

        # Adding field 'PlayerHistory.seperate_rank'
        db.add_column(u'league_playerhistory', 'seperate_rank',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)

        # Adding field 'Player.attacker_mu'
        db.add_column(u'league_player', 'attacker_mu',
                      self.gf('django.db.models.fields.FloatField')(default=25.0),
                      keep_default=False)

        # Adding field 'Player.attacker_sigma'
        db.add_column(u'league_player', 'attacker_sigma',
                      self.gf('django.db.models.fields.FloatField')(default=8.333333333333334),
                      keep_default=False)

        # Adding field 'Player.attacker_rank'
        db.add_column(u'league_player', 'attacker_rank',
                      self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True),
                      keep_default=False)

        # Adding field 'Player.defender_mu'
        db.add_column(u'league_player', 'defender_mu',
                      self.gf('django.db.models.fields.FloatField')(default=25.0),
                      keep_default=False)

        # Adding field 'Player.defender_sigma'
        db.add_column(u'league_player', 'defender_sigma',
                      self.gf('django.db.models.fields.FloatField')(default=8.333333333333334),
                      keep_default=False)

        # Adding field 'Player.defender_rank'
        db.add_column(u'league_player', 'defender_rank',
                      self.gf('django.db.models.fields.FloatField')(default=0.0, db_index=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'PlayerHistory.was_attacker'
        db.delete_column(u'league_playerhistory', 'was_attacker')

        # Deleting field 'PlayerHistory.seperate_mu'
        db.delete_column(u'league_playerhistory', 'seperate_mu')

        # Deleting field 'PlayerHistory.seperate_sigma'
        db.delete_column(u'league_playerhistory', 'seperate_sigma')

        # Deleting field 'PlayerHistory.seperate_rank'
        db.delete_column(u'league_playerhistory', 'seperate_rank')

        # Deleting field 'Player.attacker_mu'
        db.delete_column(u'league_player', 'attacker_mu')

        # Deleting field 'Player.attacker_sigma'
        db.delete_column(u'league_player', 'attacker_sigma')

        # Deleting field 'Player.attacker_rank'
        db.delete_column(u'league_player', 'attacker_rank')

        # Deleting field 'Player.defender_mu'
        db.delete_column(u'league_player', 'defender_mu')

        # Deleting field 'Player.defender_sigma'
        db.delete_column(u'league_player', 'defender_sigma')

        # Deleting field 'Player.defender_rank'
        db.delete_column(u'league_player', 'defender_rank')


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
            'Meta': {'ordering': "['name']", 'object_name': 'Player'},
            'attacker_mu': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'attacker_rank': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'attacker_sigma': ('django.db.models.fields.FloatField', [], {'default': '8.333333333333334'}),
            'defender_mu': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'defender_rank': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'defender_sigma': ('django.db.models.fields.FloatField', [], {'default': '8.333333333333334'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mu': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'rank': ('django.db.models.fields.FloatField', [], {'default': '0.0', 'db_index': 'True'}),
            'sigma': ('django.db.models.fields.FloatField', [], {'default': '8.333333333333334'})
        },
        u'league.playerhistory': {
            'Meta': {'object_name': 'PlayerHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.Match']"}),
            'mu': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['league.Player']"}),
            'rank': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'seperate_mu': ('django.db.models.fields.FloatField', [], {'default': '25.0'}),
            'seperate_rank': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'seperate_sigma': ('django.db.models.fields.FloatField', [], {'default': '8.333333333333334'}),
            'sigma': ('django.db.models.fields.FloatField', [], {'default': '8.333333333333334'}),
            'was_attacker': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['league']