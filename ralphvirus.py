import os
import sys
import random
import string
import keyboard
import time
from config import STOP_CODE

class Keyboardjoke:
    """System-wide keyboard letter corruption joke."""
    
    def __init__(self):
        self.suppressing = False
        self.running = True
        self.typed_buffer = ""
        self.stop_code = STOP_CODE  # loaded from config.py
        print("[*] Keyboard malware initialized")
        print(f"[*] Type '{self.stop_code}' to stop")
    
    def on_key_event(self, event):
        """Global keyboard key handler."""
        if self.suppressing:
            return False
        
        try:
            # Only process key press events (not release)
            if event.event_type == keyboard.KEY_DOWN:
                char = event.name
                
                # Only process single letter keys
                if len(char) == 1 and char.isalpha():
                    # Track typed characters for stop code
                    self.typed_buffer += char.lower()
                    if len(self.typed_buffer) > len(self.stop_code):
                        self.typed_buffer = self.typed_buffer[-len(self.stop_code):]
                    
                    # Check if stop code was typed
                    if self.typed_buffer == self.stop_code:
                        print(f"\n[!] STOPPED - Stop code '{self.stop_code}' entered")
                        self.stop()
                        return False
                    
                    # Determine case
                    if char.isupper():
                        letters = string.ascii_uppercase
                    else:
                        letters = string.ascii_lowercase
                    
                    # Get a random letter that's NOT the one typed
                    replacement = random.choice(letters.replace(char, ""))
                    
                    print(f"[*] Typed: '{char}' -> Replaced with: '{replacement}'")
                    
                    # Delete the original character and type replacement
                    self.suppressing = True
                    time.sleep(0.01)
                    keyboard.press_and_release('backspace')
                    time.sleep(0.05)
                    keyboard.write(replacement)
                    time.sleep(0.05)
                    self.suppressing = False
                    return False
                    
        except Exception as e:
            self.suppressing = False
            print(f"[!] Error: {e}")

    
    def start(self):
        """Start the global keyboard listener."""
        self.running = True
        print("[+] Listening to all keyboard input globally...")
        print(f"[+] Type '{self.stop_code}' to stop\n")
        self.listener = keyboard.on_press(self.on_key_event)
        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Stop the malware."""
        self.running = False
        keyboard.unhook_all()
        print("[*] Keyboard malware stopped safely")
        sys.exit(0)


if __name__ == "__main__":
    malware = Keyboardjoke()
    try:
        malware.start()
    except KeyboardInterrupt:
        malware.stop()