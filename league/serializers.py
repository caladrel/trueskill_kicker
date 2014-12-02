from rest_framework import serializers

from league.models import Match, Player


class MatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Match


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
