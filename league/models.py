from django.core.validators import MaxValueValidator
from django.db import models


class Player(models.Model):
    name = models.CharField(max_length=200)
    name.db_index = True
    mu = models.FloatField(default=25.0)
    sigma = models.FloatField(default=25. / 3.)
    rank = models.FloatField(default=0.0)
    rank.db_index = True

    attacker_mu = models.FloatField(default=25.0)
    attacker_sigma = models.FloatField(default=25. / 3.)
    attacker_rank = models.FloatField(default=0.0)
    attacker_rank.db_index = True

    defender_mu = models.FloatField(default=25.0)
    defender_sigma = models.FloatField(default=25. / 3.)
    defender_rank = models.FloatField(default=0.0)
    defender_rank.db_index = True

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('league:player_detail', args=[str(self.id)])

    def matches_attacker_count(self):
        return self.playerhistory_set.filter(was_attacker=True).count()

    def matches_defender_count(self):
        return self.playerhistory_set.filter(was_attacker=False).count()


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


class PlayerHistory(models.Model):
    player = models.ForeignKey(Player)
    player.db_index = True
    mu = models.FloatField(default=25.0)
    sigma = models.FloatField(default=25. / 3.)
    rank = models.FloatField(default=0.0)
    match = models.ForeignKey(Match)

    was_attacker = models.BooleanField()

    seperate_mu = models.FloatField(default=25.0)
    seperate_sigma = models.FloatField(default=25. / 3.)
    seperate_rank = models.FloatField(default=0.0)
