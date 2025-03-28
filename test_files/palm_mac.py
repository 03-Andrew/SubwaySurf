import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)

clicking = False
smooth_x, smooth_y = screen_width // 2, screen_height // 2
alpha = 0.2  # Smoothing factor

def is_palm_closed(landmarks):
    tips = [8, 12, 16, 20]
    closed = 0
    for tip in tips:
        if landmarks[tip].y > landmarks[tip - 2].y:
            closed += 1
    return closed >= 3

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            x = int(hand_landmarks.landmark[0].x * w)
            y = int(hand_landmarks.landmark[0].y * h)

            # Map relative to frame center to screen center
            relative_x = (x - w / 2) / (w / 2)  # -1 to 1
            relative_y = (y - h / 2) / (h / 2)

            target_x = screen_width / 2 + (relative_x * screen_width / 2)
            target_y = screen_height / 2 + (relative_y * screen_height / 2)

            # Smooth movement
            smooth_x = alpha * target_x + (1 - alpha) * smooth_x
            smooth_y = alpha * target_y + (1 - alpha) * smooth_y

            pyautogui.moveTo(smooth_x, smooth_y)

            # Click detection
            if is_palm_closed(hand_landmarks.landmark):
                if not clicking:
                    pyautogui.click()
                    clicking = True
            else:
                clicking = False

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Mouse", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
