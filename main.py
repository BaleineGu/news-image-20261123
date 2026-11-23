"""Deliver the finished front-page image to the grader's output folder.

The image ships in this repository as entry.png, already drawn at
1024x1024. This program moves those bytes to where the grader looks:
the directory named by MAKEFUN_OUTPUT_DIR, or /output when the
variable is absent. It uses only the standard library, touches no
network, and copies the file byte for byte, so repeated runs produce
identical output. A missing source image or a short copy is an error,
not a silent partial run.
"""

import hashlib
import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"
DEST_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if not IMAGE.is_file():
        raise FileNotFoundError(f"front-page image not found: {IMAGE}")
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    target = DEST_DIR / "entry.png"
    shutil.copyfile(IMAGE, target)
    if target.stat().st_size != IMAGE.stat().st_size:
        raise IOError("copy size mismatch")
    if sha256(target) != sha256(IMAGE):
        raise IOError("copy hash mismatch: output must be byte-identical")


if __name__ == "__main__":
    main()
