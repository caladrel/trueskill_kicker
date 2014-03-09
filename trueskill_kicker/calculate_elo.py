import math
import scraper


def round_like_php(x):
    if x > 0:
        return math.floor(x + 0.5)
    else:
        return math.ceil(x - 0.5)

_, results = scraper.scrape_matches(history=True)

elo = {}

for result in reversed(results):
    p0, p1 = result[0].split(' / ')
    p2, p3 = result[1].split(' / ')
    s0, s1 = map(int, result[2].split(':'))

    # if result is draw, ignore it
    if s0 == s1:
        continue

    elo0 = .5 * (elo.get(p0, 1200) + elo.get(p1, 1200))
    elo1 = .5 * (elo.get(p2, 1200) + elo.get(p3, 1200))

    # expected probability of team 2 winning
    p = 1. / (1. + 10. ** ((elo0 - elo1) / 400.))

    # team 2 wins
    if s1 > s0:
        # minus expected probability of team 1 winning
        p = p - 1

    change = round_like_php(25. * p)

    if change == 0:
        change = math.copysign(1, p)

    elo[p0] = elo.get(p0, 1200) + change
    elo[p1] = elo.get(p1, 1200) + change
    elo[p2] = elo.get(p2, 1200) - change
    elo[p3] = elo.get(p3, 1200) - change

for score, player in reversed(sorted((v, k) for k, v in elo.iteritems())):
    print player, score
