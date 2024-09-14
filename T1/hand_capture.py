import cv2
import mediapipe as mp
from typing import Optional, Tuple


MAX_HAND_COUNT = 1

class HandLandmark:
    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z


class HandLandmarks:
    wrist: Optional[HandLandmark]
    thumb_tip: Optional[HandLandmark]
    index_tip: Optional[HandLandmark]

    def __init__(self,
                 wrist: Optional[HandLandmark],
                 index_tip: Optional[HandLandmark],
                 thumb_tip: Optional[HandLandmark] = None,
                 ):
        self.wrist = wrist
        self.thumb_tip = thumb_tip
        self.index_tip = index_tip


# Initialize MediaPipe Hands and drawing utils
mp_hands = mp.solutions.hands.Hands(
    max_num_hands=MAX_HAND_COUNT,  # Detect up to 1 hand
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils


def get_hand_landmarks(frame: cv2.Mat) -> Optional[HandLandmarks]:
    # Convert the image to RGB (MediaPipe requires RGB input)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and detect hands
    results = mp_hands.process(rgb_frame)

    hand_landmarks = None

    # Draw the hand annotations on the image if hands are detected
    if results.multi_hand_landmarks:
        for i, multi_hand_landmarks in enumerate(results.multi_hand_landmarks):
            if i >= MAX_HAND_COUNT:
                print(f"Only {MAX_HAND_COUNT} hand(s) are supported.")
                break
            mp_drawing.draw_landmarks(frame, multi_hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

            # Get coordinates of key points on the hand (e.g., wrist, index finger tip)
            wrist = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
            wrist_landmark = HandLandmark(wrist.x, wrist.y, wrist.z)

            thumb_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            thumb_tip_landmark = HandLandmark(thumb_tip.x, thumb_tip.y, thumb_tip.z)
            
            index_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            index_tip_landmark = HandLandmark(index_tip.x, index_tip.y, index_tip.z)

            hand_landmarks = HandLandmarks(
                wrist_landmark,
                thumb_tip_landmark,
                index_tip_landmark,
            )

    return hand_landmarks


def is_grabbing(hand_landmarks: HandLandmarks) -> bool:
    if hand_landmarks is None:
        return False

    # Calculate the distance between the thumb tip and the index finger tip
    thumb_tip = hand_landmarks.thumb_tip
    index_tip = hand_landmarks.index_tip
    if thumb_tip is None or index_tip is None:
        return False

    distance_squared = (
        (thumb_tip.x - index_tip.x) ** 2 +
        (thumb_tip.y - index_tip.y) ** 2 +
        (thumb_tip.z - index_tip.z) ** 2
    )
    distance = distance_squared ** 0.5

    return distance < 0.1


if __name__ == "__main__":
    # Set up webcam
    cap: cv2.VideoCapture = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        exit()

    hand_landmarks = None
    
    ret: bool
    frame: Optional[cv2.Mat]
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        frame = cv2.flip(frame, 1)  # Mirror the frame
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

    cap.release()
    cv2.destroyAllWindows()
