import sys
from importlib import import_module
import os
from queue import Queue
from random import random, randint, shuffle
from threading import Barrier, Lock
from turtle import Screen, tracer, update

from typing import Union, Tuple, Callable

from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.match import run_match
import turtle_programs
from turtle_game.player import Player
from turtle_game.stoppable_thread import StoppableThread
from turtle_game.world import World
from turtle_game.world_dimensions import WorldDimensions


def check_color_tuple(color_tuple):
    valid = True
    for val in color_tuple:
        valid &= isinstance(val,float)
    return valid
def default_placement_function(world: World) -> Tuple[float, float]:
    num = randint(0,1)
    location = world.random_location()
    if num == 0:
        location = (world.world_dimensions.max_x() if randint(0,1) == 0 else world.world_dimensions.min_x(), location[1])
    else:
        location = (location[0], world.world_dimensions.max_y() if randint(0,1) == 0 else world.world_dimensions.min_y())
    return location

def default_movement_function(turtle: CompetitionTurtle, world: World):
    turtle.forward(turtle.energy_level())

def test_function(function, *arguments):
    try:
        function(*arguments)
    except:
        pass
def test_function_time(time: float, function: Callable, *arguments):
    for i in range(100):
        try:
            test_thred = StoppableThread(target=test_function, args=(function,*arguments,))
            test_thred.start()
            test_thred.join(time)
            if test_thred.is_alive():
                test_thred.stop()
                return False
        except:
            pass
    return True

def can_goto( turtle: CompetitionTurtle):
    return False
def game_over():
    return False if randint(0,1)==1 else True
def get_bool(prey: CompetitionTurtle):
    return False if randint(0,1)==1 else True




def failsafes(person):
    team_name: str
    color: Union[str,Tuple[float,float,float]]
    placement_function: Callable[[World, int],Tuple[float, float]]
    movement_function: Callable[[CompetitionTurtle, World], None]

    if not hasattr(person,"team_name") or not isinstance(person.team_name,str):
        print("Team name falesafe triggered")
        team_name = "Untitled Team"
    else:
        team_name = person.team_name
    if not (hasattr(person,"color")  and (isinstance(person.color, str) or (isinstance(person.color, Tuple) and len(person.color) == 3 and check_color_tuple(person.color)))):
        print("Color falesafe triggered")
        color = "blue"
    else:
        color = person.color
    if not hasattr(person,"placement_function") or not isinstance(person.placement_function, Callable):
        print("Placement function failsafe 1 triggered")
        placement_function = default_placement_function
    else:
        placement_function = person.placement_function
    test_turtle = CompetitionTurtle(team_name, color, World().random_location()[0], World().random_location()[1], Barrier(1)
                                    , Barrier(1), Queue(), {team_name:[]}, Lock(), Lock(), can_goto, game_over ,get_bool, get_bool, get_bool, get_bool, get_bool, get_bool, get_bool, get_bool, 12)
    test_turtle.hide()
    if not hasattr(person,"movement_function") or not isinstance(person.movement_function, Callable) :
        print("Movement function failsafe 1 triggered")
        movement_function = default_movement_function
    else:
        movement_function = person.movement_function
    return Player(team_name,color,placement_function,movement_function)

Screen().setup(width=0, height=0)
people=[]

for file in os.listdir(turtle_programs.__path__[0]):
    if file.endswith(".py") and file != "__init__.py":
        person = import_module("turtle_programs."+ file.replace(".py","").strip())
        person = failsafes(person)
        people.append(person)

Screen().setup(width=1.0, height=1.0)
people_per_match = 2
round = 1
shuffle(people)
while len(people) > 1:
    winners = []
    for i in range(0,len(people),people_per_match):
        players = []
        for k in range(people_per_match):
            if (i + k < len(people)):
                players.append(people[(i + k)])
            else:
                break
        if len(players) == 1:
            if not (players[0] in winners):
                winners.append(players[0])
            continue
        input("Hit any key to clear last match: ")
        update()
        tracer(0,0)
        update()
        Screen().setup(width=1.0-random()/100, height=1.0-random()/100)
        print("round " + str(round) + " match " + str(i // people_per_match + 1))
        for player in players:
            print(player.team_name,player.color)
        winner = run_match(players)
        print("Winner:",winner.team_name,str(winner.color))
        if not (winner in winners):
            winners.append(winner)
    people = winners
    shuffle(people)
    round += 1
print("Congratulations",people[0].team_name + " won the tournament" if len(people) > 0 else "everyone won because we all learned")
Screen().exitonclick()

