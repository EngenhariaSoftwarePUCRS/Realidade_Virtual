import cv2
import mediapipe as mp
from typing import Optional, Tuple


class HandLandmark:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


Wrists = Tuple[Optional[HandLandmark], Optional[HandLandmark]]


# Initialize MediaPipe Hands and drawing utils
mp_hands = mp.solutions.hands.Hands(
    max_num_hands=2,  # Detect up to two hands
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils


def get_wrists_location(frame: cv2.Mat) -> Wrists:
    wrists_locations = [None, None]

    # Convert the image to RGB (MediaPipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = mp_hands.process(rgb_frame)

    # Draw the hand annotations on the image if hands are detected
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            if i >= 2:
                print("Only two hands are supported.")
                break
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # Get coordinates of key points on the hand (e.g., wrist)
            wrist = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
            wrists_locations[i] = HandLandmark(x=wrist.x, y=wrist.y, z=wrist.z)

    return tuple(wrists_locations)


if __name__ == "__main__":
    # Set up webcam
    cap: cv2.VideoCapture = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        exit()

    wrists_locations: Wrists = (None, None)
    
    ret: bool
    frame: Optional[cv2.Mat]
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        frame = cv2.flip(frame, 1)  # Mirror the frame
        wrists_locations = get_wrists_location(frame)

        if any(wrist is not None for wrist in wrists_locations):
            wrists_count = len([wrist for wrist in wrists_locations if wrist is not None])
            print(f"\nHands detected: {wrists_count}")

            for i, wrist_location in enumerate(wrists_locations):
                if wrist_location is not None:
                    print(f"Wrist {i + 1} found at: {wrist_location.x:.2f}, {wrist_location.y:.2f}, {wrist_location.z:.2f}")

        cv2.imshow("Hands Seeker", frame)
        
        # Press 'q' to exit the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
