import cv2
from typing import Optional

from hand_capture import HandLandmarks, get_hand_landmarks, is_grabbing
from objects_render import init as init_render

# Set up display window size
display = (640, 360)

# Set up webcam
cap = cv2.VideoCapture(0)

# Initialize global variables
hand_landmarks: HandLandmarks = None


def main():
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        exit()

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
            print(f"\nHand detected")
            wrist_location = hand_landmarks.wrist
            print(f"Wrist found at: {wrist_location.x:.2f}, {wrist_location.y:.2f}, {wrist_location.z:.2f}")
            print(f"Thumb tip found at: {hand_landmarks.thumb_tip.x:.2f}, {hand_landmarks.thumb_tip.y:.2f}, {hand_landmarks.thumb_tip.z:.2f}")
            print(f"Index finger tip found at: {hand_landmarks.index_tip.x:.2f}, {hand_landmarks.index_tip.y:.2f}, {hand_landmarks.index_tip.z:.2f}")

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
