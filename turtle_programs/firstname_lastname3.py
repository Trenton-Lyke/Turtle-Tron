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
    if turtle.is_turtle_on_left_edge():
        turtle.setheading(0)
        turtle.forward(turtle.max_speed())
    elif turtle.is_turtle_on_top_edge():
        turtle.setheading(270)
        turtle.forward(turtle.max_speed())
    elif turtle.is_turtle_on_right_edge():
        turtle.setheading(180)
        turtle.forward(turtle.max_speed())
    elif turtle.is_turtle_on_bottom_edge():
        turtle.setheading(90)
        turtle.forward(turtle.max_speed())
    else:
        angle = turtle.closest_enemy_predator().angle()+180
        turtle.setheading(angle)
        turtle.forward(turtle.energy_level()/2)

def predator_movement_function(turtle: CompetitionTurtle, world: World):
    angle = turtle.closest_enemy_prey().angle()
    turtle.setheading(angle)
    turtle.forward(turtle.energy_level()/2)