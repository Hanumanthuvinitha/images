import os
import json
import subprocess

# Set your repo path here
repo_path = r"C:\Users\palap\Downloads\esp32cam\images"

# Step 1: Change to the repo directory
os.chdir(repo_path)

# Step 2: List all .jpg files
jpg_files = [f for f in os.listdir(repo_path) if f.lower().endswith(".jpg")]

# Step 3: Write them to images.json
with open("images.json", "w") as f:
    json.dump(jpg_files, f, indent=2)

# Step 4: Run Git commands to add, commit, and push
def run_git_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)

# Add .jpg files and images.json
run_git_command("git add *.jpg images.json")

# Commit
run_git_command('git commit -m "Auto-upload images and update images.json"')

# Push
run_git_command("git push origin main")
