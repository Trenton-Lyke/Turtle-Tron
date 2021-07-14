from __future__ import annotations
from math import sqrt
from typing import Tuple



class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, point: Point):
        return sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def __str__(self):
        return "("+str(self.x)+","+str(self.y)+")"

class PointPair:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2


    def distToSegment(self, point: Point):
        l2 = dist2(self.point1, self.point2)
        if l2 == 0:
            return sqrt(dist2(point, self.point1))
        t = ((point.x - self.point1.x) * (self.point2.x - self.point1.x) + (point.y - self.point1.y) * (self.point2.y - self.point1.y)) / l2
        t = max(0, min(1, t))
        return sqrt(dist2(point, Point(self.point1.x + t * (self.point2.x - self.point1.x), self.point1.y + t * (self.point2.y - self.point1.y))))


    def is_on_line(self, point, line_range=12):
        return self.distToSegment(point) < line_range

def tuple_to_point(point: Tuple[float, float]) -> Point:
    return Point(point[0], point[1])

def tuples_to_point_pair(point1: Tuple[float,float], point2: Tuple[float,float]) -> PointPair:
    return PointPair(tuple_to_point(point1),tuple_to_point(point2))
def dist2(v, w):
    return (v.x - w.x)**2 + (v.y - w.y)**2

