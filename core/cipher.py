# ─────────────────────────────────────────────────────────────
# core/cipher.py
# Key derivation + Encryption pipeline stages.
# Logic bilkul original se hai — kuch change nahi kiya.
# ─────────────────────────────────────────────────────────────

import hashlib
import struct
from typing import List, Optional

from config.settings import CONFIG


# ── Extended-GCD based modular inverse (MOD=256 ke liye) ────
def _modinv(a: int, m: int) -> int:
    """Modular inverse via extended Euclidean algorithm.
    Works for any m (prime ho ya na ho), sirf gcd(a,m)==1 chahiye."""
    g, x, _ = _extended_gcd(a % m, m)
    if g != 1:
        raise ValueError("Inverse does not exist")
    return x % m


def _extended_gcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    g, x, y = _extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


# ─────────────────────────────────────────────────────────────
# KEY ENGINE
# ─────────────────────────────────────────────────────────────
class KEY_ENGINE:
    def __init__(self, SECRET: str):
        self.SECRET = SECRET.encode()
        self._KEYS: Optional[List[bytes]] = None

    def DERIVE(self) -> List[bytes]:
        if self._KEYS:
            return self._KEYS

        DATA = self.SECRET + CONFIG.SALT
        for _ in range(CONFIG.KDF_ROUNDS):
            DATA = hashlib.sha256(DATA).digest()

        KEYS = []
        for I in range(CONFIG.SUBKEYS):
            KEYS.append(hashlib.sha256(DATA + struct.pack(">I", I)).digest())

        self._KEYS = KEYS
        return KEYS

    def CHANNEL_KEYS(self):
        K = self.DERIVE()
        return (
            struct.unpack(">I", K[0][:4])[0],
            struct.unpack(">I", K[1][:4])[0],
            struct.unpack(">I", K[2][:4])[0],
        )

    def SHUFFLE_SEED(self, I: int):
        K = self.DERIVE()
        return struct.unpack(">I", K[3 + I % (len(K) - 3)][:4])[0]

    def AFFINE_KEYS(self):
        K = self.DERIVE()
        A = struct.unpack(">I", K[6][:4])[0] | 1
        B = struct.unpack(">I", K[7][:4])[0]
        return A % (CONFIG.MOD - 1), B


# ─────────────────────────────────────────────────────────────
# PIPELINE STAGE 1 — Channel XOR
# ─────────────────────────────────────────────────────────────
class CHANNEL_STAGE:
    @staticmethod
    def APPLY(PIXELS, KE: KEY_ENGINE):
        RK, GK, BK = KE.CHANNEL_KEYS()
        OUT = []
        for I, (R, G, B) in enumerate(PIXELS):
            P = I & 0xFF
            OUT.append((
                R ^ ((RK + P) & 0xFF),
                G ^ ((GK + P) & 0xFF),
                B ^ ((BK + P) & 0xFF),
            ))
        return OUT


# ─────────────────────────────────────────────────────────────
# PIPELINE STAGE 2 — Pixel Shuffle (LCG-based)
# ─────────────────────────────────────────────────────────────
class SHUFFLE_STAGE:
    A = 1664525
    C = 1013904223
    M = 2 ** 32

    @staticmethod
    def SHUFFLE(PIXELS, SEED):
        N = len(PIXELS)
        IDX = list(range(N))
        S = SEED
        for I in range(N - 1, 0, -1):
            S = (SHUFFLE_STAGE.A * S + SHUFFLE_STAGE.C) % SHUFFLE_STAGE.M
            J = S % (I + 1)
            IDX[I], IDX[J] = IDX[J], IDX[I]
        return [PIXELS[I] for I in IDX], IDX

    @staticmethod
    def UNSHUFFLE(PIXELS, IDX):
        INV = [0] * len(IDX)
        for I, J in enumerate(IDX):
            INV[J] = I
        return [PIXELS[INV[I]] for I in range(len(INV))]


# ─────────────────────────────────────────────────────────────
# PIPELINE STAGE 3 — Affine Transform
# ─────────────────────────────────────────────────────────────
class VALUE_STAGE:
    @staticmethod
    def APPLY(PIXELS, KE: KEY_ENGINE):
        A, B = KE.AFFINE_KEYS()
        return [(
            (R  * A + B) % CONFIG.MOD & 0xFF,
            (G  * A + B) % CONFIG.MOD & 0xFF,
            (BL * A + B) % CONFIG.MOD & 0xFF,
        ) for R, G, BL in PIXELS]

    @staticmethod
    def REVERSE(PIXELS, KE: KEY_ENGINE):
        A, B   = KE.AFFINE_KEYS()
        INV_A  = _modinv(A, CONFIG.MOD)          # extended-GCD inverse
        return [(
            (R  - B) * INV_A % CONFIG.MOD & 0xFF,
            (G  - B) * INV_A % CONFIG.MOD & 0xFF,
            (BL - B) * INV_A % CONFIG.MOD & 0xFF,
        ) for R, G, BL in PIXELS]
