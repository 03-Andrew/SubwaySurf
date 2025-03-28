from pynput.keyboard import Controller, Key
import time

class PoseController:
    def __init__(self, cooldown, column_map):
        self.keyboard = Controller()
        self.last_column = 'center'
        self.last_move_time = 0
        self.last_jump_time = 0
        self.last_duck_time = 0
        self.action_color = (255, 255, 255)  # Default white
        self.cooldown = cooldown
        self.column_map = column_map

    def get_column(self, x, width):
        if x < width / 3:
            return 'left'
        elif x > 2 * width / 3:
            return 'right'
        else:
            return 'center'

    def handle_movement(self, chest_x, width):
        current_time = time.time()
        current_column = self.get_column(chest_x, width)

        if current_column != self.last_column and current_time - self.last_move_time > self.cooldown:
            diff = self.column_map[current_column] - self.column_map[self.last_column]
            if diff != 0:
                direction = Key.right if diff > 0 else Key.left
                for _ in range(abs(diff)):
                    self.keyboard.press(direction)
                    self.keyboard.release(direction)
                    print(f"{'➡️' if direction == Key.right else '⬅️'} Move {'Right' if direction == Key.right else 'Left'}")
                    time.sleep(0.05)
                self.last_move_time = current_time
                self.action_color = (0, 255, 0)  # Green for movement
            self.last_column = current_column

    def handle_jump(self, left_wrist_y, right_wrist_y, chest_y):
        current_time = time.time()
        if left_wrist_y < chest_y and right_wrist_y < chest_y and current_time - self.last_jump_time > self.cooldown:
            self.keyboard.press(Key.up)
            self.keyboard.release(Key.up)
            print("⬆️ Jump")
            self.last_jump_time = current_time
            self.action_color = (0, 255, 255)  # Yellow for jump

    def handle_duck(self, ls_y, rs_y, height):
        current_time = time.time()
        if ls_y > height // 2 and rs_y > height // 2 and current_time - self.last_duck_time > self.cooldown:
            self.keyboard.press(Key.down)
            self.keyboard.release(Key.down)
            print("⬇️ Duck (Shoulders Low)")
            self.last_duck_time = current_time
            self.action_color = (0, 0, 255)  # Red for duck

