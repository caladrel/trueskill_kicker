from django.core.validators import MaxValueValidator
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    mu = models.FloatField(default=25.0)
    sigma = models.FloatField(default=25. / 3.)
    rank = models.FloatField(default=0.0)
    rank.db_index = True

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('league:player_detail', args=[str(self.id)])


class Match(models.Model):
    score_team1 = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10)],
        choices=[(i, i) for i in xrange(11)])
    score_team2 = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(10)],
        choices=[(i, i) for i in xrange(11)])
    team1_player1 = models.ForeignKey(Player, related_name='+')
    team1_player2 = models.ForeignKey(Player, related_name='+')
    team2_player1 = models.ForeignKey(Player, related_name='+')
    team2_player2 = models.ForeignKey(Player, related_name='+')
    timestamp = models.DateTimeField(auto_now_add=True)
    timestamp.db_index = True

    class Meta:
        verbose_name_plural = "matches"

    def __unicode__(self):
        return '%s / %s vs. %s / %s (%d:%d)' % (
            self.team1_player1, self.team1_player2,
            self.team2_player1, self.team2_player2,
            self.score_team1, self.score_team2)
