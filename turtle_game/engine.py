from math import sqrt, degrees, atan2
from queue import Queue
from random import random, randint
from threading import Barrier, Lock, Thread, Event
from typing import Tuple, List, Callable, Dict
from turtle import tracer, update

from turtle_game.Point import PointPair, tuple_to_point
from turtle_game.competition_turtle import CompetitionTurtle
from turtle_game.relative_location import RelativeLocation
from turtle_game.game_data_entry import GameDataEntry

from turtle_game.player import Player
from turtle_game.stoppable_thread import StoppableThread
from turtle_game.world import World





class Engine:
    def __init__(self, world: World, players: List[Player], border_proximity:float=10, own_line_deaths:bool=False, safe_mode:bool=False):
        self.safe_mode = safe_mode
        self.world: World = world
        self.players: List[Player] = players
        parties = len(players) + 1
        self.move_barrier: Barrier = Barrier(parties)
        self.check_barrier: Barrier = Barrier(parties)
        self.process_queue: Queue = Queue()
        self.line_lists: Dict[str, List[PointPair]] = {}
        for player in players:
            self.line_lists[player.team_name] = []
        self.game_lock: Lock = Lock()
        self.line_lock: Lock = Lock()
        self.movement_functions_dict: Dict[str, Callable[[CompetitionTurtle], None]] = {}
        self.__border_proximity = border_proximity
        self.__own_line_deaths = own_line_deaths
        self.__start: bool = False



        for player in players:
            tracer(0, 0)
            self.movement_functions_dict[player.team_name] = player.movement_function
            location = player.placement_function(self.world)
            location = self.location_failsafe(location, True)
            turtle = CompetitionTurtle(player.team_name, player.color, location[0], location[1],
                                       self.move_barrier, self.check_barrier, self.process_queue, self.line_lists,
                                       self.line_lock,self.game_lock, self.can_move_without_wait,
                                       self.game_over, self.is_turtle_on_left_edge, self.is_turtle_on_top_edge,
                                       self.is_turtle_on_right_edge, self.is_turtle_on_bottom_edge,
                                       self.is_turtle_in_top_left_corner, self.is_turtle_in_top_right_corner,
                                       self.is_turtle_in_bottom_right_corner, self.is_turtle_in_bottom_left_corner, 9)
            self.world.turtles.append(turtle)

        tracer(0, 0)
        while(not self.check_turtles(False)):
            pass
        update()

    def location_failsafe(self, location, is_prey):
        if not (isinstance(location, Tuple) and len(location) == 2 and isinstance(location[0], float) and isinstance(
                location[1], float)):
            print(("Prey" if is_prey else "Predator"),"placement function failsafe 2 triggered")
            location = self.world.random_location()
        return location


    def can_move_without_wait(self, turtle: CompetitionTurtle):
        return not self.__start or not self.world.is_in_bounds(turtle)





    def check_turtles(self, can_die: bool)->bool:
        for turtle in self.world.turtles:
            if not self.move_inbounds(turtle) and not can_die:
                return False
            if not self.update_engine_lists(can_die, turtle) and not can_die:
                return False
            turtle.enemy_relative_locations.sort(key=lambda x: x.distance())
        tracer(0, 0)
        update()
        return True



    def update_engine_lists(self, can_die: bool, turtle: CompetitionTurtle)-> bool:
        if self.is_turtle_on_line( turtle):
            if can_die:
                turtle.hide()
                self.world.turtles[:] = [x for x in self.world.turtles if not x == turtle]
                print(turtle.team_name(), "died")
                return True
            else:
                location = self.world.random_location()
                turtle.goto(location[0], location[1])
                return False
        turtle.enemy_relative_locations = []
        for other_turtle in self.world.turtles:
            if turtle != other_turtle:
                distance = turtle.distance(other_turtle)
                angle = turtle.angle(other_turtle)
                turtle.enemy_relative_locations.append(RelativeLocation(angle, distance))

        return True

    def is_turtle_on_line(self, turtle: CompetitionTurtle):
        turtle_on_line = False
        for player in self.players:
            if player.team_name != turtle.team_name():
                for line in self.line_lists[player.team_name]:
                    if(line.is_on_line(tuple_to_point(turtle.position()))):
                        return True
            elif self.__own_line_deaths:
                touched_line_before = False
                is_touching_current_line = False
                for line in self.line_lists[player.team_name]:
                    just_touched_line = line.is_on_line(tuple_to_point(turtle.position()))
                    if just_touched_line:
                        if not touched_line_before:
                            touched_line_before = True
                            is_touching_current_line = True
                    elif is_touching_current_line:
                        return True
                    else:
                        pass
        return False

    def move_inbounds(self, turtle):
        x = turtle.position()[0]
        y = turtle.position()[1]
        stayed = True
        if x > self.world.world_dimensions.max_x():
            turtle.force_heading(360-(turtle.heading()+180))
            turtle.goto(self.world.world_dimensions.max_x(), y)
            stayed = False
        elif x < self.world.world_dimensions.min_x():
            turtle.force_heading(360 - (turtle.heading()+180))
            turtle.goto(self.world.world_dimensions.min_x(), y)
            stayed = False
        if y > self.world.world_dimensions.max_y():
            turtle.force_heading(360 - turtle.heading())
            turtle.goto(x, self.world.world_dimensions.max_y())
            stayed = False
        elif y < self.world.world_dimensions.min_y():
            turtle.force_heading(360 - turtle.heading())
            turtle.goto(x, self.world.world_dimensions.min_y())
            stayed = False
        return stayed



    def game_over(self) -> bool:
        return len(self.world.turtles) <= 1

    def is_turtle_on_left_edge(self, turtle: CompetitionTurtle) -> bool:
        return abs(turtle.position()[0]-self.world.world_dimensions.min_x()) < self.__border_proximity
    def is_turtle_on_top_edge(self, turtle: CompetitionTurtle) -> bool:
        return abs(turtle.position()[1] - self.world.world_dimensions.max_y()) < self.__border_proximity
    def is_turtle_on_right_edge(self, turtle: CompetitionTurtle) -> bool:
        return abs(turtle.position()[0] - self.world.world_dimensions.max_x()) < self.__border_proximity
    def is_turtle_on_bottom_edge(self, turtle: CompetitionTurtle) -> bool:
        return abs(turtle.position()[1] - self.world.world_dimensions.min_y()) < self.__border_proximity
    def is_turtle_in_top_left_corner(self, turtle: CompetitionTurtle) -> bool:
        return self.is_turtle_on_left_edge(turtle) and self.is_turtle_on_top_edge(turtle)
    def is_turtle_in_top_right_corner(self, turtle: CompetitionTurtle) -> bool:
        return self.is_turtle_on_right_edge(turtle) and self.is_turtle_on_top_edge(turtle)
    def is_turtle_in_bottom_right_corner(self, turtle: CompetitionTurtle) -> bool:
        return self.is_turtle_on_right_edge(turtle) and self.is_turtle_on_bottom_edge(turtle)
    def is_turtle_in_bottom_left_corner(self, turtle: CompetitionTurtle) -> bool:
        return self.is_turtle_on_left_edge(turtle) and self.is_turtle_on_bottom_edge(turtle)
    def winning_player(self) -> Player:
        if (len(self.world.turtles) == 1):
            return [player for player in self.players if player.team_name == self.world.turtles[0].team_name()][0]
        print("It was a draw selecting random winner...")
        return self.players[randint(0,len(self.players))]

    def turtle_thread_function(self, function: Callable[[CompetitionTurtle, World], None], turtle: CompetitionTurtle):
        invalid_function: bool = False
        while not self.game_over():
            if not invalid_function:
                turtle.reset_wait()
                try:
                    if self.safe_mode:
                        test_thred = StoppableThread(target=function, args=(turtle, self.world,))
                        test_thred.start()

                        while test_thred.is_alive():
                            Event().wait(timeout=.25)
                            if not turtle.did_wait():
                                turtle.wait()
                                test_thred.stop()
                                invalid_function = True
                    else:
                        function(turtle, self.world)
                except Exception as e:
                    print(e)
                    turtle.wait()
                if not turtle.did_wait():
                    print("Turtle movement function failsafe 2 triggered (turtle did not wait)")
                    turtle.wait()
            else:
                print("Turtle movement function failsafe 3 triggered (turtle took too long to decide turn) shutting down turtle behavior")
                turtle.wait()

    def start_threads(self):
        for turtle in self.world.turtles:
            turtle.start()
            thread = Thread(target=(self.turtle_thread_function), args=(self.movement_functions_dict[turtle.team_name()], turtle))
            thread.setDaemon(True)
            thread.start()

    def run(self):
        self.__start = True
        self.start_threads()
        old_count = len(self.world.turtles)
        while not self.game_over():
            try:
                self.move_barrier.wait()
            except:
                pass
            tracer(0, 0)
            while not self.process_queue.empty():
                command = self.process_queue.get()
                command.function(command.value)

            self.check_turtles(True)
            update()
            try:
                self.check_barrier.wait()
            except:
                pass
        tracer(0, 0)
        update()
        winner = self.winning_player()
        print("Winner:",winner.team_name,str(winner.color))
        return self.winning_player()



