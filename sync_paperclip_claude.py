import os
import time
import shutil

source_cred = r"C:\Users\mateu\.claude\.credentials.json"
watch_dir = r"C:\Users\mateu\.paperclip\instances\default\ai-local-logins"

os.makedirs(watch_dir, exist_ok=True)

print("Starting Paperclip Claude credentials sync watcher...")
while True:
    try:
        if os.path.exists(watch_dir) and os.path.exists(source_cred):
            for item in os.listdir(watch_dir):
                subpath = os.path.join(watch_dir, item)
                if os.path.isdir(subpath):
                    target1 = os.path.join(subpath, ".credentials.json")
                    target2 = os.path.join(subpath, "credentials.json")
                    if not os.path.exists(target1) or os.path.getsize(target1) == 0:
                        shutil.copy2(source_cred, target1)
                        print(f"Copied to {target1}")
                    if not os.path.exists(target2) or os.path.getsize(target2) == 0:
                        shutil.copy2(source_cred, target2)
                        print(f"Copied to {target2}")
    except Exception as e:
        print("Watcher error:", e)
    time.sleep(1)
