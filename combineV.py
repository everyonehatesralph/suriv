import subprocess
import sys
import keyboard
import time

# List of scripts to run
scripts = [
    "ralphvirus.py",
    "cursorRus.py",
    "startup.py"
]

processes = []

# Start all scripts
for script in scripts:
    print(f"Starting {script}")
    p = subprocess.Popen([sys.executable, script])
    processes.append(p)

print("All scripts running. Press ESC to stop everything.")

# Wait until ESC is pressed
keyboard.wait("esc")

print("ESC pressed. Stopping all scripts...")

# Terminate all processes
for p in processes:
    p.terminate()

print("All scripts stopped.")