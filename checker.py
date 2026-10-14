
import hashlib
import json
import os
import sys

HASH_FILE = "hashes.json"
EXCLUDED_DIRS = {".git", "__pycache__", ".venv", "venv"}


def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)

    return digest.hexdigest()


def collect_files(paths):
    for path in paths:
        if os.path.isfile(path):
            if os.path.basename(path) != HASH_FILE:
                yield path

        elif os.path.isdir(path):
            for root, dirs, files in os.walk(path):
                dirs[:] = [
                    name for name in dirs
                    if name not in EXCLUDED_DIRS
                ]

                for name in files:
                    if name != HASH_FILE:
                        yield os.path.join(root, name)

        else:
            yield path


def load_hashes():
    if os.path.exists(HASH_FILE):
        try:
            with open(HASH_FILE, "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            print("ERROR: Cannot read hashes.json")
            sys.exit(1)

    return {}


def save_hashes(hashes):
    with open(HASH_FILE, "w") as file:
        json.dump(hashes, file, indent=2)


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python checker.py save <file-or-folder> [...]")
        print("  python checker.py check <file-or-folder> [...]")
        sys.exit(1)

    action = sys.argv[1]

    if action not in ("save", "check"):
        print("Unknown action. Use save or check.")
        sys.exit(1)

    paths = list(collect_files(sys.argv[2:]))
    hashes = load_hashes()
    processed = 0

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

            processed += 1

        except OSError as error:
            print(f"ERROR: {path}: {error}")

    if action == "save":
        save_hashes(hashes)
        print("Baseline(s) saved.")

    print(f"Files processed: {processed}")


if __name__ == "__main__":
    main()
