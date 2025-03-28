from pynput.keyboard import Controller, Key
import time

keyboard = Controller()

time.sleep(3)
keyboard.press(Key.right)
keyboard.release(Key.right)
print("Pressed Right Arrow")
