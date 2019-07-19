import urllib.request

class game:
    def __init__(self, first_line):
        contents = first_line.split(" ")
        self.info = {"map":contents[0], "map_playtime":contents[1], "date": contents[2]}
        self.players = list()

    def add_player(self, player_line):
        contents = player_line.split(" ")
        self.players.append({"time_on_team": contents[0],
                             "time_total": contents[1],
                             "dplogin": contents[2]})


if __name__ == '__main__':
    fp = urllib.request.urlopen("http://whoa.gq/server-stats/server-stats1.0.txt")
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    lines = mystr.split("\n")

    new_match = False
    in_match = False
    matches = list()
    counter = -1
    for line in lines:
        if not line.startswith("#"):
            if not line:
                in_match = False
            if in_match:
                matches[counter].add_player(line)
            if new_match:
                print(line)
                matches.append(game(line))
                counter += 1
                in_match = True
                new_match = False
            if not line:
                new_match = True

    for idx, match in enumerate(matches):
        print(match.players)