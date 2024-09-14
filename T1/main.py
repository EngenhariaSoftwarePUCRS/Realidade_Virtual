import cv2
from typing import Optional

from prints import print_hand_landmarks
from hand_capture import HandLandmark, HandLandmarks, get_hand_landmarks, is_grabbing
from objects_render import (
    draw_sphere,
    init as init_render,
    glClear,
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    pygame,
)

# Set up display window size
display = (640, 360)

# Set up webcam
cap = cv2.VideoCapture(0)

# Initialize global variables
hand_landmarks: HandLandmarks = None
sphere_size = 0.2
sphere_position = [0, 0, 0]


def normalized_to_display_position(normalized_position: HandLandmark) -> tuple[int, int]:
    return (
        normalized_position.x * display[0],
        normalized_position.y * display[1],    
    )


def main():
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        exit()
    
    init_render(display)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, display[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, display[1])
    
    ret: bool
    frame: Optional[cv2.Mat]
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

            sphere_position = [
                hand_landmarks.wrist.x,
                -hand_landmarks.wrist.y,
                hand_landmarks.wrist.z,
            ]
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw_sphere([-5, 0, 0], 1, (1, 0, 0))
            draw_sphere(sphere_position, sphere_size, (0, 1, 0))
            draw_sphere([1, 0, 5], 1, (0, 0, 1))
            pygame.display.flip()

            is_grabbing_something = is_grabbing(hand_landmarks)
            print(f"Is grabbing: {is_grabbing_something}")
        

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
