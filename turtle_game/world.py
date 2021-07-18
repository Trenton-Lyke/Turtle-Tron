from random import random
from turtle import screensize, Screen
from typing import List, Tuple

from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.world_dimensions import WorldDimensions


class World:
    def __init__(self, width: int=1000, height: int=1000, background=True):
        self.world_dimensions: WorldDimensions = WorldDimensions(width,height)
        self.turtles: List[CompetitionTurtle] = []
        screensize(int(self.world_dimensions.width()), int(self.world_dimensions.height()))
        Screen().clear()
        if background:
            pass
            # Screen().bgcolor("black")

    def is_in_bounds(self, turtle: CompetitionTurtle):
        x=turtle.position()[0]
        y=turtle.position()[1]
        return x > self.world_dimensions.min_x() and x < self.world_dimensions.max_x() and y > self.world_dimensions.min_y() and y < self.world_dimensions.max_y()

    def random_location(self) -> Tuple[float,float]:
        x:float=(random()-.5)*(self.world_dimensions.max_x() - self.world_dimensions.min_x())
        y:float=(random()-.5)*(self.world_dimensions.max_y() - self.world_dimensions.min_y())
        return (x,y)









