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

def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python checker.py save <file1> [file2 ...]")
        print("  python checker.py check <file1> [file2 ...]")
        sys.exit(1)

    action = sys.argv[1]
    paths = sys.argv[2:]
    hashes = load_hashes()

    if action not in ("save", "check"):
        print("Unknown action. Use save or check.")
        sys.exit(1)

    for path in paths:
        try:
            current_hash = sha256_file(path)

            if action == "save":
                hashes[path] = current_hash
                print(f"SAVED: {path}")

            else:
                saved_hash = hashes.get(path)

                if saved_hash is None:
                    print(f"NO BASELINE: {path}")
                elif saved_hash == current_hash:
                    print(f"OK: {path} has not changed")
                else:
                    print(f"WARNING: {path} has changed!")

        except OSError as error:
            print(f"ERROR: {path}: {error}")

    if action == "save":
        save_hashes(hashes)
        print("Baseline(s) saved.")

if __name__ == "__main__":
    main()
