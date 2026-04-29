import cv2
import mediapipe as mp
import serial
import time

# -----------------------------
# Initialize Arduino serial
# -----------------------------
arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)
time.sleep(2)  # Give Arduino time to initialize

# -----------------------------
# Initialize Mediapipe Hands
# -----------------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# -----------------------------
# Finger detection function
# -----------------------------
def detect_fingers(hand_landmarks: mp.framework.formats.landmark_pb2.NormalizedLandmarkList, 
                   hand_label: str = "Right") -> list[int]:
    """
    Detect which fingers are up.
    Returns a list of 0 (down) or 1 (up) for Thumb, Index, Middle, Ring, Pinky.
    """
    tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0]-1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tip_ids[0]].x > hand_landmarks.landmark[tip_ids[0]-1].x else 0)

    # Other fingers
    for i in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i]-2].y else 0)

    return fingers

# -----------------------------
# Start webcam
# -----------------------------
cap = cv2.VideoCapture(0)

try:
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture frame from camera.")
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

                # Determine hand label
                hand_label = results.multi_handedness[idx].classification[0].label

                # Detect fingers
                finger_states = detect_fingers(hand_lms, hand_label)
                finger_count = sum(finger_states)

                print(f"{hand_label} hand - Finger count: {finger_count}")

                # Send to Arduino with newline
                arduino.write(f"{finger_count}\n".encode())

        cv2.imshow("Hand Tracking", img)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC key to exit
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    arduino.close()
