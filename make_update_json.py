#!/usr/bin/env python3
"""Creates update.json for the GitHub updater.

Usage:  python make_update_json.py SpeedMaxPro.apk 2 1.1 "What is new" [--force]

  argument 1  the APK file you are about to upload
  argument 2  versionCode  (the SAME number as versionCode in your build.gradle for that APK)
  argument 3  versionName  (what users see, e.g. 1.1)
  argument 4  notes shown in the update pop-up (optional)
  --force     users cannot skip this update (optional)

It fills in the APK's size and SHA-256 for you. Upload the APK and the generated update.json to the repo.
"""
import hashlib, json, os, sys

args = [a for a in sys.argv[1:] if a != "--force"]
force = "--force" in sys.argv[1:]
if len(args) < 3:
    print(__doc__)
    sys.exit(1)

apk, code, name = args[0], int(args[1]), args[2]
notes = args[3] if len(args) > 3 else ""

h = hashlib.sha256()
with open(apk, "rb") as f:
    for chunk in iter(lambda: f.read(1 << 20), b""):
        h.update(chunk)

out = {
    "versionCode": code,
    "versionName": name,
    "apk": os.path.basename(apk),
    "sha256": h.hexdigest(),
    "size": os.path.getsize(apk),
    "notes": notes.replace("\\n", "\n"),
    "force": force,
}
with open("update.json", "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("update.json written:")
print(json.dumps(out, indent=2, ensure_ascii=False))
