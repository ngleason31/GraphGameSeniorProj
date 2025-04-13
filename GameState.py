import Planet
import Ship

class GameState:
    def __init__(self, planets, ships, scoreboard_data):
        self.planets = planets
        self.ships = ships
        self.scoreboard = scoreboard_data

    def to_dict(self):
        return {
            "planets": [p.serialize() for p in self.planets],
            "ships": [s.serialize() for s in self.ships],
            "scoreboard": self.scoreboard,
        }

    @staticmethod
    def from_dict(data):
        # deserialize planets and ships
        planets = [Planet.deserialize(p) for p in data["planets"]]
        ships = [Ship.deserialize(s) for s in data["ships"]]
        return GameState(planets, ships, data["scoreboard"])