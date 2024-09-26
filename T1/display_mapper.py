from OpenGL.GL import *
from OpenGL.GLU import *

from points import Point, Point2D, Point3D


smallest_allowed_depth = -1e-7
largest_allowed_depth = 1e7
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
        min_capture_found: float,
        max_capture_found: float,
    ) -> float:
        """Normalize and invert the depth of the hand landmark."""

        # Ensure the depth is within the min/max allowed range
        hand_landmark_depth = max(smallest_allowed_depth, min(largest_allowed_depth, hand_landmark_depth))

        depth = max(min_capture_found, min(max_capture_found, hand_landmark_depth))
        depth = depth - min_capture_found

        range_found = max_capture_found - min_capture_found
        normalized_depth = depth / range_found

        # Clamp the result between 0 and 1 (just in case)
        normalized_depth = max(0.0, min(1.0, normalized_depth))

        return 1 - normalized_depth


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
