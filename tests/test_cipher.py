# ─────────────────────────────────────────────────────────────
# tests/test_cipher.py
# python -m pytest tests/   (project root se chalayen)
# ─────────────────────────────────────────────────────────────

import sys, os, tempfile, unittest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image
from core.image_loader import IMAGE_CIPHER


def _make_test_image(path: str, w: int = 4, h: int = 4):
    """Small synthetic RGB image banana — koi external file nahi chahiye."""
    pixels = [(i * 16 % 256, i * 32 % 256, i * 48 % 256) for i in range(w * h)]
    img = Image.new("RGB", (w, h))
    img.putdata(pixels)
    img.save(path, "PNG")
    return pixels


class TestRoundTrip(unittest.TestCase):
    """Encrypt → Decrypt ke baad original pixels milne chahiye."""

    def setUp(self):
        self.tmp   = tempfile.TemporaryDirectory()
        self.src   = os.path.join(self.tmp.name, "original.png")
        self.enc   = os.path.join(self.tmp.name, "encrypted.png")
        self.dec   = os.path.join(self.tmp.name, "decrypted.png")
        self.key   = "test_secret_key"
        self.orig  = _make_test_image(self.src)
        self.cipher = IMAGE_CIPHER()

    def tearDown(self):
        self.tmp.cleanup()

    # ── basic round-trip ─────────────────────────────────────
    def test_encrypt_decrypt_roundtrip(self):
        self.cipher.ENCRYPT(self.src, self.enc, self.key)
        self.cipher.DECRYPT(self.enc, self.dec, self.key)

        recovered = list(Image.open(self.dec).convert("RGB").getdata())
        self.assertEqual(self.orig, recovered)

    # ── encrypted != original ────────────────────────────────
    def test_encrypted_differs_from_original(self):
        self.cipher.ENCRYPT(self.src, self.enc, self.key)

        enc_pixels = list(Image.open(self.enc).convert("RGB").getdata())
        self.assertNotEqual(self.orig, enc_pixels)

    # ── galat key se decrypt nahi hona chahiye ──────────────
    def test_wrong_key_fails_roundtrip(self):
        self.cipher.ENCRYPT(self.src, self.enc, self.key)
        self.cipher.DECRYPT(self.enc, self.dec, "wrong_key")

        recovered = list(Image.open(self.dec).convert("RGB").getdata())
        self.assertNotEqual(self.orig, recovered)

    # ── image size preserve honi chahiye ─────────────────────
    def test_image_size_preserved(self):
        self.cipher.ENCRYPT(self.src, self.enc, self.key)

        orig_size = Image.open(self.src).size
        enc_size  = Image.open(self.enc).size
        self.assertEqual(orig_size, enc_size)


class TestKeyEngine(unittest.TestCase):
    """KEY_ENGINE unit tests."""

    def test_derive_returns_correct_count(self):
        from core.cipher import KEY_ENGINE
        ke = KEY_ENGINE("hello")
        keys = ke.DERIVE()
        self.assertEqual(len(keys), 16)   # CONFIG.SUBKEYS = 16

    def test_derive_is_deterministic(self):
        from core.cipher import KEY_ENGINE
        ke1 = KEY_ENGINE("same")
        ke2 = KEY_ENGINE("same")
        self.assertEqual(ke1.DERIVE(), ke2.DERIVE())

    def test_different_secrets_give_different_keys(self):
        from core.cipher import KEY_ENGINE
        ke1 = KEY_ENGINE("alpha")
        ke2 = KEY_ENGINE("beta")
        self.assertNotEqual(ke1.DERIVE(), ke2.DERIVE())


if __name__ == "__main__":
    unittest.main()
