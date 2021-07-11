from __future__ import annotations
from math import sqrt, atan2, degrees
from queue import Queue
from threading import Lock, Barrier
from turtle import Turtle

from typing import Union, Callable, List, Tuple, Dict

from turtle_game.Point import PointPair, tuple_to_point
from turtle_game.command import Command
from turtle_game.relative_location import RelativeLocation



class CompetitionTurtle:
    def __init__(self, team_name: str, color: Union[str,Tuple[float,float,float]], x: float, y: float, move_barrier: Barrier, check_barrier: Barrier, process_queue: Queue, line_lists: Dict[str,List[PointPair]], process_lock: Lock, line_lock: Lock, can_move_without_wait: Callable[[CompetitionTurtle], bool], is_game_over: Callable[[], bool], is_turtle_on_left_edge: Callable[[CompetitionTurtle], bool], is_turtle_on_top_edge: Callable[[CompetitionTurtle], bool], is_turtle_on_right_edge: Callable[[CompetitionTurtle], bool], is_turtle_on_bottom_edge: Callable[[CompetitionTurtle], bool], is_turtle_in_top_left_corner: Callable[[CompetitionTurtle], bool], is_turtle_in_top_right_corner: Callable[[CompetitionTurtle], bool], is_turtle_in_bottom_right_corner: Callable[[CompetitionTurtle], bool], is_turtle_in_bottom_left_corner: Callable[[CompetitionTurtle], bool], max_speed: float):
        self.__turtle: Turtle = Turtle()
        self.__turtle.shape('turtle')
        self.__team_name: str = team_name
        self.__turtle.speed("fastest")
        self.__turtle.color(color)
        self.__turtle.pencolor(color)
        self.__turtle.pensize(10)
        self.__turtle.shapesize(2)
        self.__turtle.penup()
        self.__move_barrier: Barrier = move_barrier
        self.__check_barrier: Barrier = check_barrier
        self.__process_queue: Queue = process_queue
        self.__line_lists: Dict[str,List[PointPair]] = line_lists
        self.__process_lock: Lock = process_lock
        self.__line_lock: Lock = line_lock
        self.enemy_relative_locations: List[RelativeLocation] = []
        self.__energy: int = 5
        self.__started: bool = False
        self.__can_move_without_wait: Callable[[CompetitionTurtle], bool] = can_move_without_wait
        self.__waited = False
        self.__is_alive = True
        self.goto(x, y)
        self.__max_speed: float = max_speed
        self.__is_game_over: Callable[[],bool] = is_game_over
        self.__is_turtle_on_left_edge: Callable[[CompetitionTurtle],bool] = is_turtle_on_left_edge
        self.__is_turtle_on_top_edge: Callable[[CompetitionTurtle],bool] = is_turtle_on_top_edge
        self.__is_turtle_on_right_edge: Callable[[CompetitionTurtle],bool] = is_turtle_on_right_edge
        self.__is_turtle_on_bottom_edge: Callable[[CompetitionTurtle],bool] = is_turtle_on_bottom_edge
        self.__is_turtle_in_top_left_corner: Callable[[CompetitionTurtle],bool] = is_turtle_in_top_left_corner
        self.__is_turtle_in_top_right_corner: Callable[[CompetitionTurtle],bool] = is_turtle_in_top_right_corner
        self.__is_turtle_in_bottom_right_corner: Callable[[CompetitionTurtle],bool] = is_turtle_in_bottom_right_corner
        self.__is_turtle_in_bottom_left_corner: Callable[[CompetitionTurtle],bool] = is_turtle_in_bottom_left_corner


    def start(self):
        self.__started = True
        self.__turtle.pendown()



    def team_name(self) -> str:
        return self.__team_name

    def reset_wait(self):
        self.__waited = False


    def __add_to_process_queue(self, function: Callable[[float], None], value: float):
        if self.__is_alive:
            self.__process_lock.acquire()
            self.__process_queue.put(Command(function, value))
            self.__process_lock.release()

    def __add_to_line_lists(self, point1, point2):
        if self.__is_alive:
            self.__line_lock.acquire()
            self.__line_lists[self.__team_name].append(PointPair(point1,point2))
            self.__line_lock.release()

    def __add_point_to_line_lists(self, point):
        if self.__is_alive:
            self.__add_to_line_lists(point, point)

    def __add_current_point_to_line_lists(self):
        if self.__is_alive:
            self.__add_point_to_line_lists(tuple_to_point(self.position()))

    def __change_last_line_endpoint(self, point2):
        if self.__is_alive:
            self.__line_lock.acquire()
            self.__line_lists[self.__team_name].append(PointPair(self.__line_lists[self.__team_name].pop().point1,point2))
            self.__line_lock.release()

    def __change_last_line_endpoint_to_current(self):
        if self.__is_alive:
            self.__change_last_line_endpoint(tuple_to_point(self.position()))

    def wait(self, bonus=True):
        if bonus:
            self.__energy += 10
        else:
            self.__energy += 5
        self.__just_ate = False
        try:
            self.__move_barrier.wait()
        except Exception as e:
            print(e)
        try:
            self.__check_barrier.wait()
        except Exception as e:
            print(e)
        self.__waited = True

    def did_wait(self):
        return self.__waited
    def forward(self, speed: float):
        if self.__is_alive:
            speed = min(speed, self.__energy, self.__max_speed)
            self.__energy -= speed
            self.__add_to_process_queue(self.__turtle.forward, speed)
        self.wait(False)
        self.__change_last_line_endpoint_to_current()

    def backward(self, speed: float):
        if self.__is_alive:
            speed = min(speed, self.__energy, self.__max_speed)
            self.__energy -= speed
            self.__add_to_process_queue(self.__turtle.backward, speed)
        self.wait(False)
        self.__change_last_line_endpoint_to_current()

    def right(self, value: float):
        if self.__is_alive:
            if self.__energy >= 1:
                self.__energy -= 1
                self.__add_to_process_queue(self.__turtle.right, value)
        self.wait(False)
        self.__add_current_point_to_line_lists()

    def left(self, value: float):
        if self.__is_alive:
            if self.__energy >= 1:
                self.__energy -= 1
                self.__add_to_process_queue(self.__turtle.left, value)
        self.wait(False)
        self.__add_current_point_to_line_lists()

    def setheading(self, value: float):
        if self.__is_alive:
            if self.__energy >= 1:
                self.__energy -= 1
                self.__add_to_process_queue(self.__turtle.setheading, value % 360)
        self.wait(False)
        self.__add_current_point_to_line_lists()

    def position(self)->(float,float):
        return self.__turtle.position()

    def goto(self, x: float, y: float, ):
        if self.__can_move_without_wait(self):
            try:
                self.__turtle.goto(x,y)
                self.__add_current_point_to_line_lists()
            except Exception as e:
                print(e)
                print("You not allowed to use the goto() method in your turtle program")
                pass
        else:
            self.wait()

    def force_heading(self, angle: float):
        if self.__can_move_without_wait(self):
            try:
                self.__turtle.setheading(angle)
                self.__add_current_point_to_line_lists()
            except:
                print("You not allowed to use the force_heading() method in your turtle program")
                pass
        else:
            self.wait()
    def hide(self):
        self.__turtle.hideturtle()
        self.__turtle.penup()
        self.__is_alive = False



    def distance(self, turtle2: CompetitionTurtle)->float:
        x1 = self.position()[0]
        y1 = self.position()[1]
        x2 = turtle2.position()[0]
        y2 = turtle2.position()[1]
        return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def angle(self, turtle2: CompetitionTurtle) -> float:
        x1 = self.position()[0]
        y1 = self.position()[1]
        x2 = turtle2.position()[0]
        y2 = turtle2.position()[1]
        return (degrees(atan2((y2 - y1), (x2 - x1))) + 360) % 360

    def energy_level(self):
        return self.__energy

    def closest_enemy(self) -> RelativeLocation:
        if len(self.enemy_relative_locations) > 0:
            return self.enemy_relative_locations[0]
        else:
            return RelativeLocation(1,1)

    def angle_to_closest_enemy(self) -> float:
        return self.closest_enemy().angle()

    def distance_to_closest_enemy(self) -> float:
        return self.closest_enemy().distance()


    def turn_to_closest_enemy(self):
        self.setheading(self.angle_to_closest_enemy())



    def max_speed(self) -> float:
        return self.__max_speed

    def is_turtle_on_left_edge(self) -> bool:
        return self.__is_turtle_on_left_edge(self)
    def is_turtle_on_top_edge(self) -> bool:
        return self.__is_turtle_on_top_edge(self)
    def is_turtle_on_right_edge(self) -> bool:
        return self.__is_turtle_on_right_edge(self)
    def is_turtle_on_bottom_edge(self) -> bool:
        return self.__is_turtle_on_bottom_edge(self)
    def is_turtle_in_top_left_corner(self) -> bool:
        return self.__is_turtle_in_top_left_corner(self)
    def is_turtle_in_top_right_corner(self) -> bool:
        return self.__is_turtle_in_top_right_corner(self)
    def is_turtle_in_bottom_right_corner(self) -> bool:
        return self.__is_turtle_in_bottom_right_corner(self)
    def is_turtle_in_bottom_left_corner(self) -> bool:
        return self.__is_turtle_in_bottom_left_corner(self)
    def heading(self) -> float:
        return self.__turtle.heading()
