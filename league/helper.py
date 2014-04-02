from django.db import transaction

from league.models import Player, Match, PlayerHistory
from trueskill import Rating, rate


def refresh_scores():
    player_dict = {p.pk: p for p in Player.objects.all()}
    rating_dict = {pk: Rating() for pk in player_dict}
    match_list = Match.objects.order_by('timestamp')

    histories = []

    for match in match_list:
        player_ids = (match.team1_player1_id, match.team1_player2_id,
                      match.team2_player1_id, match.team2_player2_id)

        ratings = [rating_dict[id] for id in player_ids]
        ranks = [match.score_team2 > match.score_team1,
                 match.score_team2 < match.score_team1]
        new_ratings = rate([ratings[0:2], ratings[2:4]], ranks=ranks)
        new_ratings = new_ratings[0] + new_ratings[1]
        for i in range(len(player_ids)):
            rating = new_ratings[i]
            rating_dict[player_ids[i]] = rating
            history = PlayerHistory()
            history.match = match
            history.player = player_dict[player_ids[i]]
            history.mu = rating.mu
            history.sigma = rating.sigma
            history.rank = rating.mu - 3 * rating.sigma
            histories.append(history)

    with transaction.atomic():
        PlayerHistory.objects.all().delete()
        PlayerHistory.objects.bulk_create(histories)
        for pk, player in player_dict.iteritems():
            rating = rating_dict[pk]
            player.mu = rating.mu
            player.sigma = rating.sigma
            player.rank = rating.mu - 3 * rating.sigma
            player.save()
