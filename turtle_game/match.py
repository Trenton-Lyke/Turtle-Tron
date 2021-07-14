from random import randint
from turtle import Screen
from typing import List

from turtle_game.engine import Engine
from turtle_game.player import Player
from turtle_game.world import World

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()1234567890_+-={[]}:?><,./|~`"

def randAdd():
    toReturn = ""
    has_dot = False
    for i in range(randint(1, 7)):
        num = randint(1, 3)

        if num == 1:
            val = randint(0, len(alphabet))
            toReturn += alphabet[val:randint(val, len(alphabet))]
        elif num == 2:
            toReturn = toReturn + str(randint(0, 9))
        elif not has_dot:
            if randint(0,1) == 0:
                toReturn = toReturn + "." +str(randint(0, 9))
            else:
                toReturn = toReturn + "." + alphabet[randint(0, len(alphabet))]
            has_dot = True
    return toReturn
def randPass(minLen):
    toReturn = ""
    while len(toReturn) < minLen:
        num = randint(0,3)
        if num < 2:
            val = randint(0, len(alphabet))
            toReturn += alphabet[val:randint(val, len(alphabet))]
        elif num == 2:
            toReturn += randAdd()
        else:
            scs = "!@#$%^&*()_+-=~`|\\/?,<>;:'\"[]\{\}"
            toReturn += scs[randint(0,len(scs)-1)]
    return toReturn

def run_match(people, world_width: int=1000, world_height: int=1000, predator_kill_radius=30, prey_per_team:int=45, predators_per_team:int=5, background=True, own_line_deaths=False) -> Player:
    players: List[Player] = []
    team_names: List[str] = []
    for person in people:
        players.append(Player((person.team_name + randPass(5)) if person.team_name in team_names else person.team_name, person.color, person.placement_function, person.movement_function))
        team_names.append(person.team_name)
    world: World = World(world_width,world_height,background)
    engine: Engine = Engine(world, players,10,own_line_deaths)
    winner: Player = engine.run()
    return winner