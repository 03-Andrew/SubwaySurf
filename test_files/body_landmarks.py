import cv2
import mediapipe as mp
import keyboard
import time

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(model_complexity=0)
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

last_column = 'center'
last_move_time = 0
last_jump_time = 0
last_duck_time = 0
cooldown = 0.25  # Faster response

column_map = {'left': 0, 'center': 1, 'right': 2}

def get_column(x, width):
    if x < width / 3:
        return 'left'
    elif x > 2 * width / 3:
        return 'right'
    else:
        return 'center'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb)

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
        current_time = time.time()

        if current_column != last_column and current_time - last_move_time > cooldown:
            if abs(column_map[current_column] - column_map[last_column]) == 1:
                if column_map[current_column] > column_map[last_column]:
                    keyboard.send('right')
                    print("➡️ Move Right")
                else:
                    keyboard.send('left')
                    print("⬅️ Move Left")
                last_move_time = current_time

            last_column = current_column

        # ===== Jump Detection =====
        if lw_y < nose_y and rw_y < nose_y and current_time - last_jump_time > cooldown:
            keyboard.send('up')
            print("⬆️ Jump")
            last_jump_time = current_time

        # ===== Duck Detection =====
        if ls_y > height // 2 and rs_y > height // 2 and current_time - last_duck_time > cooldown:
            keyboard.send('down')
            print("⬇️ Duck (Shoulders Low)")
            last_duck_time = current_time

        # ===== Draw Pose Landmarks =====
        mp_drawing.draw_landmarks(
            frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=1, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=1)
        )

    # ===== Draw Columns & Middle Line =====
    cv2.line(frame, (width // 3, 0), (width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 1)

    cv2.imshow("Subway Surfer Body Control", cv2.resize(frame, (320, 240)))
    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

