from typing import Union, Tuple
from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.world import World


team_name = "1"

color = "red"


def prey_movement_function(turtle: CompetitionTurtle, world: World):
    turtle.forward(turtle.energy_level()/2)

def movement_function(turtle: CompetitionTurtle, world: World):
    turtle.forward(turtle.energy_level()/2)