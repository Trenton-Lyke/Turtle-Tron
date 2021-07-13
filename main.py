import sys
from importlib import import_module
import os
from queue import Queue
from random import random, randint
from threading import Barrier, Lock
from turtle import Screen
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
    return world.random_location()

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


people=[]
for file in os.listdir(turtle_programs.__path__[0]):
    if file.endswith(".py") and file != "__init__.py":
        person = import_module("turtle_programs."+ file.replace(".py","").strip())
        person = failsafes(person)
        people.append(person)



winner = run_match(people)
Screen().exitonclick()

