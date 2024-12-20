import cv2
import mediapipe as mp
from typing import Optional, Tuple

from display_mapper import DisplayTo3D
from points import calculate_distance, Point3D


MAX_HAND_COUNT = 1

HandLandmark = Point3D


class HandLandmarks:
    wrist: Optional[HandLandmark]
    thumb_tip: Optional[HandLandmark]
    thumb_mcp: Optional[HandLandmark]
    index_tip: Optional[HandLandmark]
    index_mcp: Optional[HandLandmark]
    middle_tip: Optional[HandLandmark]
    middle_mcp: Optional[HandLandmark]
    ring_tip: Optional[HandLandmark]
    ring_mcp: Optional[HandLandmark]
    pinky_tip: Optional[HandLandmark]
    pinky_dip: Optional[HandLandmark]
    pinky_pip: Optional[HandLandmark]
    pinky_mcp: Optional[HandLandmark]

    def __init__(self,
                 wrist: Optional[HandLandmark],
                 index_tip: Optional[HandLandmark],
                 index_mcp: Optional[HandLandmark],
                 thumb_tip: Optional[HandLandmark] = None,
                 thumb_mcp: Optional[HandLandmark] = None,
                 middle_tip: Optional[HandLandmark] = None,
                 middle_mcp: Optional[HandLandmark] = None,
                 ring_tip: Optional[HandLandmark] = None,
                 ring_mcp: Optional[HandLandmark] = None,
                 pinky_tip: Optional[HandLandmark] = None,
                 pinky_dip: Optional[HandLandmark] = None,
                 pinky_pip: Optional[HandLandmark] = None,
                 pinky_mcp: Optional[HandLandmark] = None,
                 ):
        self.wrist = wrist
        self.thumb_tip = thumb_tip
        self.thumb_mcp = thumb_mcp
        self.index_tip = index_tip
        self.index_mcp = index_mcp
        self.middle_tip = middle_tip
        self.middle_mcp = middle_mcp
        self.ring_tip = ring_tip
        self.ring_mcp = ring_mcp
        self.pinky_tip = pinky_tip
        self.pinky_dip = pinky_dip
        self.pinky_pip = pinky_pip
        self.pinky_mcp = pinky_mcp


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

            def z_fix(z: float) -> float:
                z_scaler = 10_000_000
                z_scaled = z * z_scaler
                fixed = DisplayTo3D.normalize_hand_depth(z_scaled)
                return fixed

            # Get coordinates of key points on the hand (e.g., wrist, index finger tip)
            wrist = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST]
            wrist_landmark = HandLandmark(wrist.x, wrist.y, z_fix(wrist.z))

            thumb_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
            thumb_tip_landmark = HandLandmark(thumb_tip.x, thumb_tip.y, z_fix(thumb_tip.z))
            thumb_mcp = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_MCP]
            thumb_mcp_landmark = HandLandmark(thumb_mcp.x, thumb_mcp.y, z_fix(thumb_mcp.z))
            
            index_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]
            index_tip_landmark = HandLandmark(index_tip.x, index_tip.y, z_fix(index_tip.z))
            index_mcp = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_MCP]
            index_mcp_landmark = HandLandmark(index_mcp.x, index_mcp.y, z_fix(index_mcp.z))

            middle_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP]
            middle_tip_landmark = HandLandmark(middle_tip.x, middle_tip.y, z_fix(middle_tip.z))
            middle_mcp = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_MCP]
            middle_mcp_landmark = HandLandmark(middle_mcp.x, middle_mcp.y, z_fix(middle_mcp.z))

            ring_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP]
            ring_tip_landmark = HandLandmark(ring_tip.x, ring_tip.y, z_fix(ring_tip.z))
            ring_mcp = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_MCP]
            ring_mcp_landmark = HandLandmark(ring_mcp.x, ring_mcp.y, z_fix(ring_mcp.z))

            pinky_tip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP]
            pinky_tip_landmark = HandLandmark(pinky_tip.x, pinky_tip.y, z_fix(pinky_tip.z))
            pinky_dip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_DIP]
            pinky_dip_landmark = HandLandmark(pinky_dip.x, pinky_dip.y, z_fix(pinky_dip.z))
            pinky_pip = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_PIP]
            pinky_pip_landmark = HandLandmark(pinky_pip.x, pinky_pip.y, z_fix(pinky_pip.z))
            pinky_mcp = multi_hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_MCP]
            pinky_mcp_landmark = HandLandmark(pinky_mcp.x, pinky_mcp.y, z_fix(pinky_mcp.z))

            hand_landmarks = HandLandmarks(
                wrist_landmark,
                thumb_tip_landmark,
                thumb_mcp_landmark,
                index_tip_landmark,
                index_mcp_landmark,
                middle_tip_landmark,
                middle_mcp_landmark,
                ring_tip_landmark,
                ring_mcp_landmark,
                pinky_tip_landmark,
                pinky_dip_landmark,
                pinky_pip_landmark,
                pinky_mcp_landmark,
            )

    return hand_landmarks


def get_hand_orientation(hand_landmarks: HandLandmarks) -> Tuple[float, float, float]:
    """Determines the orientation of the hand based on the location of the tip of the middle finger in relation to the wrist."""
    if hand_landmarks is None:
        return 0, 0, 0

    wrist = hand_landmarks.wrist
    middle_tip = hand_landmarks.middle_tip

    if wrist is None or middle_tip is None:
        return 0, 0, 0

    x = middle_tip.x - wrist.x
    y = middle_tip.y - wrist.y
    z = middle_tip.z - wrist.z

    return x, y, z


def is_hand_closed(
    hand_landmarks: HandLandmarks,
    wrist_treeshold: float = 0.18,
    mcp_treeshold: float = 0.12,
) -> bool:
    """Determines if the hand is closed based on the distance between the wrist and the fingertips."""

    if hand_landmarks is None:
        return False
    
    wrist = hand_landmarks.wrist
    if wrist is None:
        return False
    
    # Calculate distances between the wrist and each fingertip
    thumb_wrist_dist = calculate_distance(hand_landmarks.thumb_tip, wrist)
    index_wrist_dist = calculate_distance(hand_landmarks.index_tip, wrist)
    middle_wrist_dist = calculate_distance(hand_landmarks.middle_tip, wrist)
    ring_wrist_dist = calculate_distance(hand_landmarks.ring_tip, wrist)
    pinky_wrist_dist = calculate_distance(hand_landmarks.pinky_tip, wrist)

    avg_finger_wrist_dist = (thumb_wrist_dist + index_wrist_dist + middle_wrist_dist + ring_wrist_dist + pinky_wrist_dist) / 5

    # print(
    #     f"Thumb-wrist distance: {thumb_wrist_dist:.2f}, "
    #     f"Index-wrist distance: {index_wrist_dist:.2f}, "
    #     f"Middle-wrist distance: {middle_wrist_dist:.2f}, "
    #     f"Ring-wrist distance: {ring_wrist_dist:.2f}, "
    #     f"Pinky-wrist distance: {pinky_wrist_dist:.2f}, "
    #     f"Avg. finger-wrist distance: {avg_finger_wrist_dist:.2f}"
    # )

    # Calculate the distances between each tip and its corresponding mcp
    thumb_mcp_dist = calculate_distance(hand_landmarks.thumb_tip, hand_landmarks.thumb_mcp)
    index_mcp_dist = calculate_distance(hand_landmarks.index_tip, hand_landmarks.index_mcp)
    middle_mcp_dist = calculate_distance(hand_landmarks.middle_tip, hand_landmarks.middle_mcp)
    ring_mcp_dist = calculate_distance(hand_landmarks.ring_tip, hand_landmarks.ring_mcp)
    pinky_mcp_dist = calculate_distance(hand_landmarks.pinky_tip, hand_landmarks.pinky_mcp)

    avg_finger_mcp_dist = (thumb_mcp_dist + index_mcp_dist + middle_mcp_dist + ring_mcp_dist + pinky_mcp_dist) / 5

    # print(
        # f"Thumb-mcp distance: {thumb_mcp_dist:.2f}, "
        # f"Index-mcp distance: {index_mcp_dist:.2f}, "
        # f"Middle-mcp distance: {middle_mcp_dist:.2f}, "
        # f"Ring-mcp distance: {ring_mcp_dist:.2f}, "
        # f"Pinky-mcp distance: {pinky_mcp_dist:.2f}, "
        # f"Avg. finger-mcp distance: {avg_finger_mcp_dist:.2f}"
    # )

    return avg_finger_wrist_dist < wrist_treeshold or avg_finger_mcp_dist < mcp_treeshold


def is_grabbing(
    hand_landmarks: HandLandmarks,
    treeshold: float = 0.1,
) -> bool:
    """Determines if the hand is grabbing something based on the distance between the thumb tip and index finger tip."""
    if hand_landmarks is None:
        return False

    thumb_tip = hand_landmarks.thumb_tip
    index_tip = hand_landmarks.index_tip
    if thumb_tip is None or index_tip is None:
        return False

    distance = calculate_distance(thumb_tip, index_tip)

    return distance < treeshold


def is_pinky_grabbing(
    hand_landmarks: HandLandmarks,
    treeshold: float = 0.1,
) -> bool:
    """Determines if the hand is grabbing something based on the distance between the thumb tip and index finger tip."""
    if hand_landmarks is None:
        return False

    thumb_tip = hand_landmarks.thumb_tip
    pinky_tip = hand_landmarks.pinky_tip
    if thumb_tip is None or pinky_tip is None:
        return False

    distance_tip = calculate_distance(thumb_tip, pinky_tip)
    distance_dip = calculate_distance(thumb_tip, hand_landmarks.pinky_dip)
    distance_pip = calculate_distance(thumb_tip, hand_landmarks.pinky_pip)
    distance_mcp = calculate_distance(thumb_tip, hand_landmarks.pinky_mcp)

    return (
        distance_tip < treeshold
        or distance_dip < treeshold
        or distance_pip < treeshold
        or distance_mcp < treeshold
    )


def is_bat_grabbing(
    hand_landmarks: HandLandmarks,
    treeshold: float = 0.15,    
) -> bool:
    """Determines if the bat is grabbing something based on the distance between the thumb tip, the middle finger tip, and the ring finger tip."""
    if hand_landmarks is None:
        return False

    thumb_tip = hand_landmarks.thumb_tip
    middle_tip = hand_landmarks.middle_tip
    ring_tip = hand_landmarks.ring_tip
    if thumb_tip is None or middle_tip is None or ring_tip is None:
        return False

    distance_thumb_middle = calculate_distance(thumb_tip, middle_tip)
    distance_thumb_ring = calculate_distance(thumb_tip, ring_tip)
    
    return distance_thumb_middle < treeshold and distance_thumb_ring < treeshold


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
            print("\n\nHand detected")
            wrist_location = hand_landmarks.wrist
            print(f"Wrist found at: {wrist_location.x:.2f}, {wrist_location.y:.2f}, {wrist_location.z:.2f}")
            # print(f"Thumb tip found at: {hand_landmarks.thumb_tip.x:.2f}, {hand_landmarks.thumb_tip.y:.2f}, {hand_landmarks.thumb_tip.z:.2f}")
            # print(f"Index finger tip found at: {hand_landmarks.index_tip.x:.2f}, {hand_landmarks.index_tip.y:.2f}, {hand_landmarks.index_tip.z:.2f}")
            # print(f"Middle finger tip found at: {hand_landmarks.middle_tip.x:.2f}, {hand_landmarks.middle_tip.y:.2f}, {hand_landmarks.middle_tip.z:.2f}")
            # print(f"Ring finger tip found at: {hand_landmarks.ring_tip.x:.2f}, {hand_landmarks.ring_tip.y:.2f}, {hand_landmarks.ring_tip.z:.2f}")
            # print(f"Pinky finger tip found at: {hand_landmarks.pinky_tip.x:.2f}, {hand_landmarks.pinky_tip.y:.2f}, {hand_landmarks.pinky_tip.z:.2f}")

            is_hand_closed_gesture = is_hand_closed(hand_landmarks)
            print(f"\nIs hand closed: {is_hand_closed_gesture}")

            is_grabbing_something = is_grabbing(hand_landmarks)
            print(f"\nIs grabbing: {is_grabbing_something}")

            is_pinky_grabbing_something = is_pinky_grabbing(hand_landmarks)
            print(f"\nIs pinky grabbing: {is_pinky_grabbing_something}")

            is_bat_grabbing_something = is_bat_grabbing(hand_landmarks)
            print(f"\nIs bat grabbing: {is_bat_grabbing_something}")

        cv2.imshow("Hands Seeker", frame)
        
        # Press 'q' to exit the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
