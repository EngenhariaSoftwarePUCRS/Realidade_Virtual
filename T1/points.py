import math
from typing import Union


class Point2D():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return f"x={self.x:.4f}, y={self.y:.4f}"

    def __repr__(self):
        return "Point2D(%.2f, %.2f)" % (self.x, self.y)
    
    def to_list(self) -> list[float]:
        return [self.x, self.y]


class Point3D(Point2D):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

    def __str__(self) -> str:
        return super().__str__() + f", z={self.z}"

    def __repr__(self):
        return "Point3D(%.4f, %.4f, %.4f)" % (self.x, self.y, self.z)
    
    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]
    
    def to_point2d(self):
        return Point2D(self.x, self.y)


Point = Union[Point2D, Point3D]


def calculate_distance(point1: Point3D, point2: Point3D) -> float:
    """Calculates the Euclidean distance between two 3D points."""
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2 + (point2.z - point1.z) ** 2)


def calculate_rotation_angle(vector: Point3D) -> float:
    magnitude = math.sqrt(vector.x ** 2 + vector.y ** 2 + vector.z ** 2)
    scaler = 200
    return magnitude * scaler
