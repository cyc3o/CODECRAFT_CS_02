# ─────────────────────────────────────────────────────────────
# core/image_loader.py
# Image load, save, encrypt, decrypt — original IMAGE_CIPHER class.
# ─────────────────────────────────────────────────────────────

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("PILLOW NOT INSTALLED. RUN: pip install Pillow")
    sys.exit(1)

from config.settings import CONFIG
from core.cipher import (
    KEY_ENGINE,
    CHANNEL_STAGE,
    SHUFFLE_STAGE,
    VALUE_STAGE,
)


class IMAGE_CIPHER:
    # ── Load ─────────────────────────────────────────────────
    def LOAD(self, PATH):
        P = Path(PATH)
        if not P.exists() or P.suffix.upper() not in CONFIG.FORMATS:
            raise ValueError("INVALID IMAGE FILE")
        IMG = Image.open(P).convert("RGB")
        return list(IMG.getdata()), IMG.size

    # ── Save ─────────────────────────────────────────────────
    def SAVE(self, PIXELS, SIZE, PATH):
        IMG = Image.new("RGB", SIZE)
        IMG.putdata(PIXELS)
        IMG.save(PATH, CONFIG.OUTPUT)

    # ── Encrypt ──────────────────────────────────────────────
    def ENCRYPT(self, SRC, DST, KEY):
        PX, SIZE = self.LOAD(SRC)
        KE = KEY_ENGINE(KEY)

        PX = CHANNEL_STAGE.APPLY(PX, KE)

        MAPS = []
        for I in range(CONFIG.SHUFFLE_PASSES):
            PX, M = SHUFFLE_STAGE.SHUFFLE(PX, KE.SHUFFLE_SEED(I))
            MAPS.append(M)

        PX = VALUE_STAGE.APPLY(PX, KE)
        self.SAVE(PX, SIZE, DST)

    # ── Decrypt ──────────────────────────────────────────────
    def DECRYPT(self, SRC, DST, KEY):
        PX, SIZE = self.LOAD(SRC)
        KE = KEY_ENGINE(KEY)

        PX = VALUE_STAGE.REVERSE(PX, KE)

        MAPS = []
        for I in range(CONFIG.SHUFFLE_PASSES):
            _, M = SHUFFLE_STAGE.SHUFFLE(PX, KE.SHUFFLE_SEED(I))
            MAPS.append(M)

        for M in reversed(MAPS):
            PX = SHUFFLE_STAGE.UNSHUFFLE(PX, M)

        PX = CHANNEL_STAGE.APPLY(PX, KE)
        self.SAVE(PX, SIZE, DST)
