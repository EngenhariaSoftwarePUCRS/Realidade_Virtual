from OpenGL.GL import *
from OpenGL.GLU import *

from points import Point, Point2D, Point3D


class DisplayTo3D:
    def __init__(self, display_size: tuple[int, int]):
        self.display_size = display_size
    
    def normalized_to_display_position(self,
        normalized_position: Point2D,
    ) -> Point2D:
        """
        Convert normalized coordinates (0-1 range) to display coordinates (OpenCV window size).
        """
        
        return Point2D(
            normalized_position.x * self.display_size[0],
            normalized_position.y * self.display_size[1],
        )
    

    def normalize_hand_depth(
        hand_landmark_depth: float,
        min_capture: float = -1_000_000,
        max_capture: float = 1_000_000,
    ) -> float:
        """Normalize and invert the depth of the hand landmark."""

        # print("\t\tHand Landmark Depth:", hand_landmark_depth)

        # Clamp the depth between the min and max capture values
        depth = max(min_capture, min(max_capture, hand_landmark_depth))
        depth = depth - min_capture

        range = max_capture - min_capture
        normalized_depth = depth / range

        # Clamp the result between 0 and 1 (just in case)
        normalized_depth = max(0.0, min(1.0, normalized_depth))

        return normalized_depth


    def convert(self,
        position: Point,
        normalized: bool = True,
        depth: float = 0.5,
    ) -> Point3D:
        """
        Convert display coordinates to 3D coordinates.
        """
        if isinstance(position, Point3D):
            depth = position.z
        
        if normalized:
            if isinstance(position, Point3D):
                position = position.to_point2d()
            position = self.normalized_to_display_position(position)

        model_view = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        win_x = position.x
        win_y = self.display_size[1] - position.y  # Invert y-axis since OpenGL origin is bottom-left
        win_z = depth
        
        world_coords = gluUnProject(win_x, win_y, win_z, model_view, projection, viewport)

        return Point3D(*world_coords)
