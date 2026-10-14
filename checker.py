import hashlib
import sys

def sha256_file(path):
    digest = hashlib.sha256()

    with open(path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            digest.update(chunk)

    return digest.hexdigest()

if len(sys.argv) != 2:
    print("Usage: python checker.py <file>")
    sys.exit(1)

try:
    print("SHA-256:", sha256_file(sys.argv[1]))
except OSError as error:
    print("Error:", error)
