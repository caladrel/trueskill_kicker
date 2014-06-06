from django.db import transaction

from league.models import Player, Match, PlayerHistory
from trueskill import Rating, rate


def refresh_scores():
    player_dict = {p.pk: p for p in Player.objects.all()}
    rating_dict = {pk: Rating() for pk in player_dict}
    attacker_rating_dict = {pk: Rating() for pk in player_dict}
    defender_rating_dict = {pk: Rating() for pk in player_dict}
    match_list = Match.objects.order_by('timestamp')

    histories = []

    for match in match_list:
        player_ids = (match.team1_player1_id, match.team1_player2_id,
                      match.team2_player1_id, match.team2_player2_id)

        ratings = [rating_dict[id] for id in player_ids]
        seperate_ratings = [
            (attacker_rating_dict[a], defender_rating_dict[d])
            for a, d in [player_ids[0:2], player_ids[2:4]]
        ]
        ranks = [match.score_team2 > match.score_team1,
                 match.score_team2 < match.score_team1]
        new_ratings = rate([ratings[0:2], ratings[2:4]], ranks=ranks)
        new_ratings = new_ratings[0] + new_ratings[1]
        new_seperate_ratings = rate(seperate_ratings, ranks=ranks)
        new_seperate_ratings = \
            new_seperate_ratings[0] + new_seperate_ratings[1]
        for i in range(len(player_ids)):
            history = PlayerHistory()

            rating = new_ratings[i]
            rating_dict[player_ids[i]] = rating
            seperate_rating = new_seperate_ratings[i]
            if not i % 2:
                history.was_attacker = True
                attacker_rating_dict[player_ids[i]] = seperate_rating
            else:
                history.was_attacker = False
                defender_rating_dict[player_ids[i]] = seperate_rating

            history.match = match
            history.player = player_dict[player_ids[i]]
            history.mu = rating.mu
            history.sigma = rating.sigma
            history.rank = rating.mu - 3 * rating.sigma
            history.seperate_mu = seperate_rating.mu
            history.seperate_sigma = seperate_rating.sigma
            history.seperate_rank = \
                seperate_rating.mu - 3 * seperate_rating.sigma
            histories.append(history)

    with transaction.atomic():
        PlayerHistory.objects.all().delete()
        PlayerHistory.objects.bulk_create(histories)
        for pk, player in player_dict.iteritems():
            rating = rating_dict[pk]
            attacker_rating = attacker_rating_dict[pk]
            defender_rating = defender_rating_dict[pk]
            player.mu = rating.mu
            player.sigma = rating.sigma
            player.rank = rating.mu - 3 * rating.sigma
            player.attacker_mu = attacker_rating.mu
            player.attacker_sigma = attacker_rating.sigma
            player.attacker_rank = \
                attacker_rating.mu - 3 * attacker_rating.sigma
            player.defender_mu = defender_rating.mu
            player.defender_sigma = defender_rating.sigma
            player.defender_rank = \
                defender_rating.mu - 3 * defender_rating.sigma
            player.save()
