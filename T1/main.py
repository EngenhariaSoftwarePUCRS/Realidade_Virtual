import cv2
from typing import Optional

from hand_capture import HandLandmarks, get_hand_landmarks, is_grabbing
from display_mapper import DisplayTo3D
from objects_render import (
    draw_sphere,
    init as init_render,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    pygame,
)
from points import Point2D
from prints import print_hand_landmarks

# Set up display window size
display = (640, 360)

# Set up webcam
cap = cv2.VideoCapture(0)

# Initialize global variables
hand_landmarks: HandLandmarks = None
sphere_size = 1 / 1_000
sphere_position = [0, 0, 0]


def main():
    global sphere_position, sphere_size
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        exit()
    
    init_render(display)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, display[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, display[1])

    display_to_3d = DisplayTo3D(display)
    
    ret: bool
    frame: Optional[cv2.Mat]

    # Draw a sphere in each of the 4 corners of the screen
    top_left = display_to_3d.convert(Point2D(-1, -1))
    top_right = display_to_3d.convert(Point2D(1, -1))
    bottom_left = display_to_3d.convert(Point2D(-1, 1))
    bottom_right = display_to_3d.convert(Point2D(1, 1))
    print(
        f"Top left: {top_left}, Top right: {top_right}, Bottom left: {bottom_left}, Bottom right: {bottom_right}"
    )
    draw_sphere(top_left, sphere_size, (1, 0, 0))
    draw_sphere(top_right, sphere_size, (0, 1, 0))
    draw_sphere(bottom_left, sphere_size, (0, 0, 1))
    draw_sphere(bottom_right, sphere_size, (1, 1, 0))
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Mirror the frame
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, display)

        hand_landmarks = get_hand_landmarks(frame)
        if hand_landmarks is not None:
            print_hand_landmarks(hand_landmarks)

            sphere_position = display_to_3d.convert(hand_landmarks.wrist)
            print(sphere_position)

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            is_grabbing_motion = is_grabbing(hand_landmarks)
            print(f"Is grabbing: {is_grabbing_motion}")

            sphere_color = (1, 0, 0) if is_grabbing_motion else (0, 1, 0)

            draw_sphere(sphere_position, sphere_size, sphere_color)

            pygame.display.flip()
        

        cv2.imshow("Hands Seeker", frame)
        
        # Press 'q' to exit the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


if __name__ == "__main__":
    try:
        main()
    finally:
        cap.release()
        cv2.destroyAllWindows()
