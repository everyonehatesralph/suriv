import ctypes
import keyboard
import threading
import time

user32 = ctypes.windll.user32

running = True

def force_hide():
    global running
    while running:
        # Keep forcing cursor hidden
        while user32.ShowCursor(False) >= 0:
            pass
        time.sleep(0.01)

def esc_listener():
    global running
    keyboard.wait("esc")
    running = False

print("Cursor will be hidden. Press ESC to stop.")

# Start hiding thread
threading.Thread(target=force_hide, daemon=True).start()

# Wait for ESC
esc_listener()

# Restore cursor
while user32.ShowCursor(True) < 0:
    pass

print("Cursor restored.")