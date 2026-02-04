# ─────────────────────────────────────────────────────────────
# config/settings.py
# App-wide constants — original CONFIG class, untouched.
# ─────────────────────────────────────────────────────────────

import os
from pathlib import Path


# ── Manual .env loader — koi external package nahi chahiye ──
def _load_env(env_path: Path):
    """Simple KEY=VALUE parser. Comments (#) + blank lines skip ho jaate hain."""
    if not env_path.exists():
        return
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


_load_env(Path(__file__).resolve().parent.parent / ".env")


class CONFIG:
    KDF_ROUNDS  = int(os.getenv("KDF_ROUNDS", 10000))
    SUBKEYS     = 16
    SHUFFLE_PASSES = 4
    MOD         = 256
    SALT        = b"IMG_CIPHER_STATIC_SALT"
    FORMATS     = {".PNG", ".JPG", ".JPEG", ".BMP", ".TIFF"}
    OUTPUT      = os.getenv("OUTPUT_FORMAT", "PNG")


# ── Terminal Colors ──────────────────────────────────────────
RESET  = "\033[0m"
WHITE  = "\033[97m"
DIM    = "\033[2m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
