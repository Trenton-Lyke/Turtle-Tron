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


    def slope(self)->float:

        return 0 if self.point2.x-self.point1.x == 0 else ((self.point2.y-self.point1.y)/(self.point2.x-self.point1.x))
    def y_intercept(self)->float:
        return self.slope()*-self.point1.x+self.point1.y
    def closest_point_on_line(self, point: Point) -> Point:
        m = self.slope()
        b = self.y_intercept()
        x = point.x
        y = point.y
        closestPoint = Point((x+m*y-m*b)/(m**2+1),m*((x+m*y+m*b)/(m**2+1))+b)

        return closestPoint


    def distToSegment(self, p):
        return sqrt(distToSegmentSquared(p, self.point1, self.point2))


    def is_on_line(self, point, line_range=12):
        return self.distToSegment(point) < line_range

    def __is_on_actual_line(self, point: Point):
        min_x = min(self.point1.x,self.point2.x)
        min_y = min(self.point1.y,self.point2.y)
        max_x = max(self.point1.x,self.point2.x)
        max_y = max(self.point1.y,self.point2.y)
        return point.x > min_x and point.x < max_x and point.y > min_y and point.y < max_y

def tuple_to_point(point: Tuple[float, float]) -> Point:
    return Point(point[0], point[1])

def tuples_to_point_pair(point1: Tuple[float,float], point2: Tuple[float,float]) -> PointPair:
    return PointPair(tuple_to_point(point1),tuple_to_point(point2))
def dist2(v, w):
    return (v.x - w.x)**2 + (v.y - w.y)**2
def distToSegmentSquared(p, v, w):
    l2 = dist2(v, w)
    if l2 == 0:
        return dist2(p, v)
    t = ((p.x - v.x) * (w.x - v.x) + (p.y - v.y) * (w.y - v.y)) / l2
    t = max(0, min(1, t))
    return dist2(p, Point(v.x + t * (w.x - v.x), v.y + t * (w.y - v.y) ))