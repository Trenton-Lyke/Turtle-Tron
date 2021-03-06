from random import random
from turtle import Turtle, screensize, Screen
from typing import List, Tuple

from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.world_dimensions import WorldDimensions


class World:
    def __init__(self, width: int=1000, height: int=1000, background=True, show_bounds=True):
        Screen().clear()
        self.show_bounds = show_bounds
        self.set_size(width,height)
        self.turtles: List[CompetitionTurtle] = []
        screensize(int(self.world_dimensions.width()), int(self.world_dimensions.height()))
        if background:
            Screen().bgcolor("black")

    def is_in_bounds(self, turtle: CompetitionTurtle):
        x=turtle.position()[0]
        y=turtle.position()[1]
        return x > self.world_dimensions.min_x() and x < self.world_dimensions.max_x() and y > self.world_dimensions.min_y() and y < self.world_dimensions.max_y()

    def random_location(self) -> Tuple[float,float]:
        x:float=(random()-.5)*(self.world_dimensions.max_x() - self.world_dimensions.min_x())
        y:float=(random()-.5)*(self.world_dimensions.max_y() - self.world_dimensions.min_y())
        return (x,y)

    def set_size(self, width, height):
        self.world_dimensions = WorldDimensions(width,height)
        if self.show_bounds:
            min_x = self.world_dimensions.min_x()
            max_x = self.world_dimensions.max_x()
            min_y = self.world_dimensions.min_y()
            max_y = self.world_dimensions.max_y()
            turtle = Turtle()
            turtle.hideturtle()
            turtle.speed(0)
            turtle.pencolor(255/255, 223/255, 79/255)
            turtle.penup()
            turtle.goto(min_x,min_y)
            turtle.pendown()
            turtle.goto(min_x,max_y)
            turtle.goto(max_x,max_y)
            turtle.goto(max_x,min_y)
            turtle.goto(min_x,min_y)









