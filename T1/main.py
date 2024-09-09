import cv2
from typing import Optional

from hand_capture import Wrists, get_wrists_location
from objects_render import init as init_render

# Set up display window size
display = (640, 360)

# Set up webcam
cap = cv2.VideoCapture(0)


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

        wrists_locations: Wrists = get_wrists_location(frame)
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


if __name__ == "__main__":
    try:
        main()
    finally:
        cap.release()
        cv2.destroyAllWindows()
