import cv2
import mediapipe as mp
import keyboard
import time

# === Setup ===
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# === Variables ===
last_column = 'center'
last_move_time = 0
last_jump_time = 0
last_duck_time = 0
cooldown = 0.2
column_map = {'left': 0, 'center': 1, 'right': 2}
prev_frame_time = 0

def get_column(x, width):
    if x < width / 3:
        return 'left'
    elif x > 2 * width / 3:
        return 'right'
    else:
        return 'center'

# === Main Loop ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)
    new_frame_time = time.time()

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        wrist = hand.landmark[0]
        palm_x = int(wrist.x * width)
        palm_y = int(wrist.y * height)
        current_time = time.time()

        # Column Movement
        current_column = get_column(palm_x, width)
        if current_column != last_column and current_time - last_move_time > cooldown:
            if column_map[current_column] > column_map[last_column]:
                keyboard.send('right')
                print("➡️ Move Right")
            else:
                keyboard.send('left')
                print("⬅️ Move Left")
            last_move_time = current_time
            last_column = current_column

        # Jump
        if palm_y < height * 0.3 and current_time - last_jump_time > cooldown:
            keyboard.send('up')
            print("⬆️ Jump")
            last_jump_time = current_time

        # Duck
        if palm_y > height * 0.75 and current_time - last_duck_time > cooldown:
            keyboard.send('down')
            print("⬇️ Duck")
            last_duck_time = current_time

        # Draw landmarks
        mp_drawing.draw_landmarks(
            frame, hand, mp_hands.HAND_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1)
        )

        # Show current column indicator
        if current_column == 'left':
            cv2.arrowedLine(frame, (30, height // 2), (80, height // 2), (0, 255, 0), 2)
        elif current_column == 'right':
            cv2.arrowedLine(frame, (width - 30, height // 2), (width - 80, height // 2), (0, 255, 0), 2)
        else:
            cv2.circle(frame, (width // 2, height // 2), 20, (0, 255, 255), 2)

    # Draw columns & thresholds
    cv2.line(frame, (width // 3, 0), (width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (0, int(height * 0.3)), (width, int(height * 0.3)), (255, 0, 0), 1)
    cv2.line(frame, (0, int(height * 0.75)), (width, int(height * 0.75)), (0, 0, 255), 1)

    # FPS
    fps = int(1 / (new_frame_time - prev_frame_time + 1e-6))
    prev_frame_time = new_frame_time
    cv2.putText(frame, f'FPS: {fps}', (10, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)

    cv2.imshow("🖐️ Subway Surfer Hand Control", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
