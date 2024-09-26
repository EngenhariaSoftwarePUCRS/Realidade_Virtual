from typing import Union


class Point2D():
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return "Point2D(%d, %d)" % (self.x, self.y)
    
    def to_list(self) -> list[float]:
        return [self.x, self.y]


class Point3D(Point2D):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self.z = z

    def __repr__(self):
        return "Point3D(%d, %d, %d)" % (self.x, self.y, self.z)
    
    def to_list(self) -> list[float]:
        return [self.x, self.y, self.z]
    
    def to_point2d(self):
        return Point2D(self.x, self.y)


Point = Union[Point2D, Point3D]
