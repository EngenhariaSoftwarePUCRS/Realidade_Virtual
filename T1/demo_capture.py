from typing import Optional
import cv2

def open_camera() -> None:
    """Opens the computer's camera and displays the video feed."""
    cap: cv2.VideoCapture = cv2.VideoCapture(0)  # 0 is usually the default camera

    if not cap.isOpened():
        print("Error: Unable to open the camera.")
        return

    while True:
        ret: bool
        frame: Optional[cv2.Mat]
        ret, frame = cap.read()  # Correctly capturing both ret and frame

        if not ret:
            print("Error: Unable to capture video.")
            break

        cv2.imshow('Camera Feed', frame)

        # Press 'q' to exit the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    open_camera()
