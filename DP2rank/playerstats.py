class PlayerStats():

    def __init__(self, name, id, kills=0, deaths=0, caps=0, grabs=0):
        self.name = name
        self.id = id
        self.kills = kills
        self.deaths = deaths
        self.caps = caps
        self.grabs = grabs

    def add_kill(self, kills=1):
        print('Player ' + self.name + ' got a point')
        self.kills += kills

    def add_capture(self, caps=1):
        print('Player ' + self.name + ' captured the flag')
        self.caps += caps

    def add_death(self, deaths=1):
        print('Player ' + self.name + ' died')
        self.deaths += deaths

    def add_grab(self, grabs=1):
        print('Player ' + self.name + ' got a grab')
        self.grabs += grabs