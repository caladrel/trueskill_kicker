from trueskill import Rating, rate
import scraper


class test:
    def __init__(self):
        self.locker_room = {}

        _, results = scraper.scrape_matches(history=True)

        for result in reversed(results):
            line = []
            line.extend(result[0].split(' / '))
            line.extend(result[1].split(' / '))
            line.extend(result[2].split(':'))
            self.process_match(line)

    def process_match(self, line):
        players = map(str, line[:4])
        score = map(int, line[4:])
        locker_room = self.locker_room
        for player in players:
            if player not in locker_room:
                locker_room[player] = Rating()
        t1 = [locker_room.pop(players[i]) for i in xrange(2)]
        t2 = [locker_room.pop(players[i]) for i in xrange(2, 4)]
        ranks = [score[1] > score[0], score[1] < score[0]]
        t1, t2 = rate([t1, t2], ranks=ranks)
        for i in xrange(2):
            locker_room[players[i]] = t1[i]
            locker_room[players[i + 2]] = t2[i]


tr = test()
i = tr.locker_room.iteritems()

for score, player in reversed(sorted((v.mu - 3 * v.sigma, k) for k, v in i)):
    print player, score
