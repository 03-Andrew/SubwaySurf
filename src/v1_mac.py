import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time

# ==== Init ====
keyboard = Controller()
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=0)

cap = cv2.VideoCapture(1, cv2.CAP_AVFOUNDATION)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

last_column = 'center'
last_move_time = 0
last_jump_time = 0
last_duck_time = 0
cooldown = 0.2  # Slightly reduced for better response

column_map = {'left': 0, 'center': 1, 'right': 2}

def get_column(x, width):
    if x < width / 3:
        return 'left'
    elif x > 2 * width / 3:
        return 'right'
    else:
        return 'center'

# ==== FPS Counter ====
fps_time = time.time()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

    current_time = time.time()

    if result.pose_landmarks:
        landmarks = result.pose_landmarks.landmark
        nose = landmarks[0]
        left_wrist = landmarks[15]
        right_wrist = landmarks[16]
        left_shoulder = landmarks[11]
        right_shoulder = landmarks[12]

        nose_x = int(nose.x * width)
        nose_y = int(nose.y * height)
        lw_y = int(left_wrist.y * height)
        rw_y = int(right_wrist.y * height)
        ls_y = int(left_shoulder.y * height)
        rs_y = int(right_shoulder.y * height)

        # ===== Column Movement =====
        current_column = get_column(nose_x, width)

        if current_column != last_column and current_time - last_move_time > cooldown:
            diff = column_map[current_column] - column_map[last_column]
            if diff != 0:
                direction = Key.right if diff > 0 else Key.left
                for _ in range(abs(diff)):
                    keyboard.press(direction)
                    keyboard.release(direction)
                    print(f"{'➡️' if direction == Key.right else '⬅️'} Move {'Right' if direction == Key.right else 'Left'}")
                    time.sleep(0.05)  # Small delay to ensure game detects double tap
                last_move_time = current_time
            last_column = current_column

        # ===== Jump Detection =====
        if lw_y < nose_y and rw_y < nose_y and current_time - last_jump_time > cooldown:
            keyboard.press(Key.up)
            keyboard.release(Key.up)
            print("⬆️ Jump")
            last_jump_time = current_time

        # ===== Duck Detection =====
        if ls_y > height // 2 and rs_y > height // 2 and current_time - last_duck_time > cooldown:
            keyboard.press(Key.down)
            keyboard.release(Key.down)
            print("⬇️ Duck (Shoulders Low)")
            last_duck_time = current_time

        # ===== Draw Pose Landmarks =====
        mp_drawing.draw_landmarks(
            frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
        )

    # ===== Draw Columns & Middle Line =====
    cv2.line(frame, (width // 3, 0), (width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 1)

    # ===== FPS =====
    fps = 1 / (current_time - fps_time)
    fps_time = current_time
    cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # ===== Show Frame =====
    cv2.imshow("Subway Surfer Body Control (Mac)", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
