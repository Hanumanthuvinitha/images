import os
import time
import json
import subprocess

WATCH_FOLDER = r"C:\esp32_audio_server"
JSON_FILE = "audio_files.json"
FILE_EXT = ".wav"
CHECK_INTERVAL = 5  # seconds
GIT_COMMIT_MSG = "Auto-commit: New .wav file(s) added and JSON updated"

# Load or create audio_files.json
json_path = os.path.join(WATCH_FOLDER, JSON_FILE)
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        try:
            audio_files = json.load(f)
        except json.JSONDecodeError:
            print("Corrupt audio_files.json, recreating.")
            audio_files = []
else:
    audio_files = []

# Track existing files
seen_files = set(audio_files)

def run_git_command(cmd_list):
    try:
        result = subprocess.run(cmd_list, cwd=WATCH_FOLDER, capture_output=True, text=True, check=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("stderr:", result.stderr)
    except subprocess.CalledProcessError as e:
        print("Git command failed:", e.stderr)

def commit_and_push(updated_files):
    for f in updated_files:
        run_git_command(["git", "add", f])
    
    run_git_command(["git", "add", JSON_FILE])  # Also add updated JSON
    run_git_command(["git", "commit", "-m", GIT_COMMIT_MSG])
    run_git_command(["git", "push"])
    print(f"Pushed {len(updated_files)} new file(s) and updated JSON.")

print("Watching for new .wav files...")

try:
    while True:
        all_files = set(f for f in os.listdir(WATCH_FOLDER) if f.endswith(FILE_EXT))
        new_files = sorted(all_files - seen_files)

        if new_files:
            print(f"New .wav files detected: {new_files}")
            
            # Update JSON
            audio_files.extend(new_files)
            with open(json_path, "w") as f:
                json.dump(audio_files, f, indent=2)
            
            # Commit and push all
            commit_and_push(new_files)
            seen_files = all_files

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("Stopped by user.")
