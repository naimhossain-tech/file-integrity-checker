import hashlib
import json
import os
import sys

HASH_FILE = "hashes.json"

def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)
    return digest.hexdigest()

def load_hashes():
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as file:
            return json.load(file)
    return {}

def save_hashes(hashes):
    with open(HASH_FILE, "w") as file:
        json.dump(hashes, file, indent=2)

if len(sys.argv) != 3:
    print("Usage:")
    print("  python checker.py save <file>")
    print("  python checker.py check <file>")
    sys.exit(1)

action, path = sys.argv[1], sys.argv[2]

try:
    current_hash = sha256_file(path)
    hashes = load_hashes()

    if action == "save":
        hashes[path] = current_hash
        save_hashes(hashes)
        print("Baseline saved.")
        print("SHA-256:", current_hash)

    elif action == "check":
        saved_hash = hashes.get(path)
        if saved_hash is None:
            print("No saved hash. Run save first.")
        elif saved_hash == current_hash:
            print("OK: File has not changed.")
        else:
            print("WARNING: File has changed!")
            print("Saved:  ", saved_hash)
            print("Current:", current_hash)

    else:
        print("Unknown action. Use save or check.")

except (OSError, json.JSONDecodeError) as error:
    print("Error:", error)
