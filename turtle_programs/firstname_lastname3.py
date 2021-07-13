from typing import Union, Tuple
from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.world import World


team_name: str = "Buffies"

color: Union[str,Tuple[float,float,float]] = "red"

def prey_placement_function(world: World, prey_number: int) -> Tuple[float, float]:
    return world.random_location()

def predator_placement_function(world: World, prey_number: int) -> Tuple[float, float]:
    return world.random_location()


def prey_movement_function(turtle: CompetitionTurtle, world: World):
    turtle.forward(turtle.energy_level()/2)

def movement_function(turtle: CompetitionTurtle, world: World):
    turtle.forward(turtle.energy_level()/2)