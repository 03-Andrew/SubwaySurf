import cv2
import mediapipe as mp
import time
import PoseController

COOLDOWN = 0.2
COLUMN_MAP = {'left': 0, 'center': 1, 'right': 2}

def draw_frame(frame, width, height):
    cv2.line(frame, (width // 3, 0), (width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (2 * width // 3, 0), (2 * width // 3, height), (0, 255, 0), 1)
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 0, 255), 1)

def draw_chest_and_wrist(controller, frame, chest_x, chest_y, lw_x, lw_y, rw_x, rw_y):
    color = controller.action_color
    cv2.line(frame, (chest_x - 10, chest_y), (chest_x + 10, chest_y), color, 2)
    cv2.line(frame, (chest_x, chest_y - 10), (chest_x, chest_y + 10), color, 2)
    cv2.circle(frame, (lw_x, lw_y), 5, color, 2)
    cv2.circle(frame, (rw_x, rw_y), 5, color, 2)

def main():
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(model_complexity=0)
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    controller = PoseController.PoseController(COOLDOWN, COLUMN_MAP)

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
            lm = result.pose_landmarks.landmark
            left_shoulder = lm[11]
            right_shoulder = lm[12]
            left_wrist = lm[15]
            right_wrist = lm[16]

            chest_x, chest_y= int((left_shoulder.x + right_shoulder.x) / 2 * width), int((left_shoulder.y + right_shoulder.y) / 2 * height)
            lw_x, lw_y = int(left_wrist.x * width), int(left_wrist.y * height)
            rw_x, rw_y = int(right_wrist.x * width), int(right_wrist.y * height)
 
            ls_y = int(left_shoulder.y * height)
            rs_y = int(right_shoulder.y * height)

                
            # Handle controls
            controller.handle_movement(chest_x, width)
            controller.handle_jump(lw_y, rw_y, chest_y)
            controller.handle_duck(ls_y, rs_y, height)

            draw_chest_and_wrist(controller, frame, chest_x, chest_y, lw_x, lw_y, rw_x, rw_y)

        draw_frame(frame, width, height)

        # FPS
        fps = 1 / (current_time - fps_time)
        fps_time = current_time
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        cv2.imshow("Body Control - Chest Mode", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
