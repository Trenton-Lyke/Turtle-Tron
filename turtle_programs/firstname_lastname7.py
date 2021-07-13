#billy_batson
from random import randint

from turtle_game.competition_turtle import CompetitionTurtle

team_namer="team name"

color = "yellow"


def prey_placement_function(world, prey_number):
    return world.random_location()

def predator_placement_function(world, prey_number):
    return world.random_location()

def movement_function(turtle: CompetitionTurtle, world):
    turtle.forward(turtle.energy_level()/2)




