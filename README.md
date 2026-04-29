# Hand Gesture Finger Counter with Arduino

A real-time hand tracking application that detects the number of raised fingers using a webcam and sends the count to an Arduino via serial communication.

---

## Overview

This project uses **MediaPipe** for hand landmark detection and **OpenCV** for webcam capture. It identifies how many fingers are held up and transmits that number over serial to an Arduino — enabling gesture-based control of hardware like LEDs, servos, or displays.

---

## Features

- Real-time hand detection and finger counting via webcam
- Supports both left and right hand detection
- Sends finger count to Arduino over serial (USB)
- Visual overlay of hand landmarks using OpenCV
- Graceful cleanup on exit (ESC key or camera failure)

---

## Requirements

### Hardware
- A webcam (built-in or USB)
- An Arduino board connected via USB (default: `COM10`)

### Python Dependencies

Install with pip:

```bash
pip install opencv-python mediapipe pyserial
```

| Package | Purpose |
|---|---|
| `opencv-python` | Webcam capture and display |
| `mediapipe` | Hand landmark detection |
| `pyserial` | Serial communication with Arduino |

---

## Setup

1. **Connect your Arduino** to your computer via USB.

2. **Find your serial port:**
   - Windows: Check Device Manager → Ports (e.g., `COM3`, `COM10`)
   - Linux/Mac: Usually `/dev/ttyUSB0` or `/dev/ttyACM0`

3. **Update the port** in the script:
   ```python
   arduino = serial.Serial(port='COM10', baudrate=9600, timeout=1)
   ```

4. **Run the script:**
   ```bash
   python hand_tracking.py
   ```

---

## How It Works

1. The webcam feed is captured frame by frame.
2. Each frame is passed to MediaPipe's hand detection model.
3. Finger states (up/down) are determined by comparing landmark positions:
   - **Thumb**: Horizontal position of tip vs. second joint (flipped for left hand)
   - **Other fingers**: Vertical position of tip vs. two joints below
4. The total finger count (0–5) is sent to the Arduino as a newline-terminated string (e.g., `"3\n"`).

---

## Controls

| Key | Action |
|---|---|
| `ESC` | Exit the program |

---

## Arduino

Your Arduino sketch should read from serial and act on the finger count. A minimal example:

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    int count = Serial.parseInt();
    // Do something with count (0–5)
  }
}
```

---

## Notes

- Only **one hand** is tracked at a time (`max_num_hands=1`).
- Detection confidence thresholds are set to `0.7` — adjust if detection is unreliable in your lighting conditions.
- The script pauses for 2 seconds on startup to give the Arduino time to initialize.

---

## License

MIT — free to use and modify.
