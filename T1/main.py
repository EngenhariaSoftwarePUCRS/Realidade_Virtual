import cv2
from random import randint
from typing import Optional

from hand_capture import HandLandmarks, get_hand_landmarks, is_grabbing
from display_mapper import DisplayTo3D
from objects_render import (
    draw_cube,
    draw_sphere,
    init as init_render,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    is_point_in_cube,
    pygame,
)
from points import Point3D
from prints import print_hand_landmarks

# Set up display window size
display = (640, 360)

# Set up webcam
cap = cv2.VideoCapture(0)

# Initialize global variables
hand_landmarks: HandLandmarks = None
sphere_size = 1 / 1_000
sphere_position = Point3D(0, 0, 0)
cube_size = 4 / 100
left_cube_position = Point3D(0.25, 0.5, 0.5)
right_cube_position = Point3D(0.75, 0.5, 0.5)


def main():
    global sphere_position, sphere_size, left_cube_position, right_cube_position

    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        exit()
    
    init_render(display)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, display[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, display[1])

    display_to_3d = DisplayTo3D(display)
    
    ret: bool
    frame: Optional[cv2.Mat]

    left_cube_position = display_to_3d.convert(left_cube_position)
    right_cube_position = display_to_3d.convert(right_cube_position)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Mirror the frame
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, display)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        draw_cube(left_cube_position, cube_size, (1, 1, 0))
        draw_cube(right_cube_position, cube_size, (0, 1, 1))

        hand_landmarks = get_hand_landmarks(frame)
        if hand_landmarks is not None:
            # print_hand_landmarks(hand_landmarks)
            sphere_position = display_to_3d.convert(hand_landmarks.wrist)
            # print(sphere_position)
            is_grabbing_motion = is_grabbing(hand_landmarks)
            #print(f"Is grabbing: {is_grabbing_motion}")
            sphere_color = (1, 0, 0) if is_grabbing_motion else (1, 1, 1)
            draw_sphere(sphere_position, sphere_size, sphere_color)

            tab_count = randint(1, 10)
            if is_point_in_cube(sphere_position, left_cube_position, cube_size):
                print("\033[1;33;40m" + "\t" * tab_count, end="")
                print("Left cube collision!")
                if is_grabbing_motion:
                    print("Left cube grabbed!")
                print("\033[0m")

            if is_point_in_cube(sphere_position, right_cube_position, cube_size):
                print("\033[1;36;40m" + "\t" * tab_count, end="")
                print("Right cube collision!")
                if is_grabbing_motion:
                    print("Right cube grabbed!")
                print("\033[0m")

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
