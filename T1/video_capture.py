import cv2
import mediapipe as mp
import time
from typing import Optional

# Initialize MediaPipe Hand detection
mp_hands: mp.solutions.hands = mp.solutions.hands
mp_drawing: mp.solutions.drawing_utils = mp.solutions.drawing_utils

# Set up webcam
cap: cv2.VideoCapture = cv2.VideoCapture(0)

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Unable to open the camera.")
    exit()

# Set up MediaPipe Hands
with mp_hands.Hands(
    max_num_hands=2,  # Detect up to two hands
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:
    while cap.isOpened():
        ret: bool
        frame: Optional[cv2.Mat]
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Flip the image horizontally for a natural selfie-view display
        frame = cv2.flip(frame, 1)

        # Convert the image to RGB (MediaPipe requires RGB input)
        rgb_frame: cv2.Mat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        # Draw the hand annotations on the image if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Get coordinates of key points on the hand (e.g., wrist, index finger)
                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                # Print wrist and index finger coordinates
                print(f"Wrist: ({wrist.x:.2f}, {wrist.y:.2f}, {wrist.z:.2f}), Index Finger: ({index_finger.x:.2f}, {index_finger.y:.2f}, {index_finger.z:.2f})")

        # Display the image with hand landmarks
        cv2.imshow('Hand Detection', frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
