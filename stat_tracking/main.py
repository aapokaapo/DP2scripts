import urllib.request
from stat_tracking import plotting


def get_file_from_web(url):
    fp = urllib.request.urlopen(url)
    mybytes = fp.read()

    mystr = mybytes.decode("utf8")
    fp.close()

    text_lines = mystr.split("\n")

    return text_lines


class game:
    def __init__(self, first_line):
        contents = first_line.split(" ")
        self.info = {"map":contents[0], "map_playtime":int(contents[1]), "date": contents[2]}
        self.players = list()

    def add_player(self, player_line):
        contents = player_line.split(" ")
        self.players.append({"time_on_team": int(contents[0]),
                             "time_total": int(contents[1]),
                             "dplogin": int(contents[2])})


def get_matches(text_lines):
    new_match = False
    in_match = False
    matches = list()
    counter = -1

    for line in text_lines:
        if not line.startswith("#"):
            if not line:
                in_match = False
            if in_match:
                matches[counter].add_player(line)
            if new_match:
                matches.append(game(line))
                counter += 1
                in_match = True
                new_match = False
            if not line:
                new_match = True
    return matches


if __name__ == '__main__':
    lines = get_file_from_web("http://whoa.gq/server-stats/server-stats1.0.txt")
    matches = get_matches(lines)
    # for match in matches:
    #     print(match.info["date"])
    plotting.seconds_per_day(matches)