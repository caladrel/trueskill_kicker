from trueskill import Rating, rate
import json


class test:
    def __init__(self):
        self.locker_room = {}

        json_data = open("data.json")

        self.data = json.load(json_data)
        json_data.close()

        for match in self.data:
            self.process_match(match)


    def process_match(self, line):
        players = map(str, line[:4])
        score = map(int, line[4:])
        locker_room = self.locker_room
        for player in players:
            if not locker_room.has_key(player):
                locker_room[player] = Rating()
        t1 = [locker_room.pop(players[i]) for i in xrange(2)]
        t2 = [locker_room.pop(players[i]) for i in xrange(2, 4)]
        ranks = [0, 0] if score[1] == score[0] else [0, 1] if score[0] > score[1] else [1, 0]
        t1, t2 = rate([t1, t2], ranks=ranks)
        for i in xrange(2):
            locker_room[players[i]] = t1[i]
            locker_room[players[i + 2]] = t2[i]


tr = test()
result = [[k, v.mu -3*v.sigma] for k, v in tr.locker_room.iteritems()]
print result