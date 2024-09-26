from hand_capture import HandLandmarks


def print_hand_landmarks(hand_landmarks: HandLandmarks) -> None:
    if hand_landmarks is None:
        return

    print(f"\nHand detected")
    wrist_location = hand_landmarks.wrist
    print(f"Wrist found at: {wrist_location.x:.2f}, {wrist_location.y:.2f}, {wrist_location.z:.2f}")
    print(f"Thumb tip found at: {hand_landmarks.thumb_tip.x:.2f}, {hand_landmarks.thumb_tip.y:.2f}, {hand_landmarks.thumb_tip.z:.2f}")
    print(f"Index finger tip found at: {hand_landmarks.index_tip.x:.2f}, {hand_landmarks.index_tip.y:.2f}, {hand_landmarks.index_tip.z:.2f}")


def print_tabs(count: int) -> None:
    print("\t" * count, end="")
