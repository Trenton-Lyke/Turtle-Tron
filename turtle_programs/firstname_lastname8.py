from typing import Union, Tuple
from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.world import World


team_name: str = "team 8"

color: Union[str,Tuple[float,float,float]] = "orange"


def prey_placement_function(world: World, prey_number: int) -> Tuple[float, float]:
    return world.random_location()

def predator_placement_function(world: World, prey_number: int) -> Tuple[float, float]:
    return world.random_location()


def movement_function(turtle: CompetitionTurtle, world: World):
    turtle.forward(turtle.energy_level()/2)

def predator_movement_function(turtle: CompetitionTurtle, world: World):
    angle = turtle.closest_enemy_prey().angle()
    turtle.setheading(angle)
    turtle.forward(turtle.energy_level()/2)