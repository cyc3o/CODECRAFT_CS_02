<H1 ALIGN="CENTER">IMAGE CIPHER</H1>
<H3 ALIGN="CENTER">SOC-STYLE </H3>

<P ALIGN="CENTER">
  <B>AUTHOR:</B> VISHAL<BR>
  <B>DOMAIN:</B> SOC • CRYPTANALYSIS • FORENSICS<BR>
  <B>LANGUAGE:</B> PYTHON
</P>

---

![ENGINE PREVIEW](https://github.com/cyc3o/CODECRAFT_CS_01/blob/9b63b9efd39e00394cec5e43e604d2a680def2f7/img/1769845510337.jpg)








## 🔐 IMAGE CIPHER

RGB PIXEL-LEVEL IMAGE ENCRYPTION — CHANNEL XOR → PIXEL SHUFFLE → AFFINE TRANSFORM

```
IMAGE_CIPHER/
├── MAIN.PY                 # 🔥 Entry Point  →  python main.py
├── REQUIREMENTS.TXT        # Dependencies
├── .ENV                    # Environment Variables (OUTPUT_FORMAT, KDF_ROUNDS)
├── .GITIGNORE
│
├── CONFIG/
│   └── SETTINGS.PY         # CONFIG Class + Terminal Colors
│
├── CORE/
│   ├── CIPHER.PY           # KEY_ENGINE + 3 Pipeline Stages
│   ├── IMAGE_LOADER.PY     # IMAGE_CIPHER (Load / Save / Encrypt / Decrypt)
│   └── UTILS.PY            # IMAGE_UTILS  (Search / Browse / Scan)
│
├── SERVICES/
│   └── IMAGE_SERVICE.PY    # Menu Handlers (Business Logic)
│
├── TESTS/
│   └── TEST_CIPHER.PY      # Round-Trip + KEY_ENGINE Unit Tests
│
└── ASSETS/
    └── SAMPLES/            # Place Your Test Images Here
---

##⚡ SETUP 

```bash
pip install -r requirements.txt
python main.py
```

---

## 🧠 HOW IT WORKS 

| Step | Stage              | Description                                                                 |
|------|--------------------|-----------------------------------------------------------------------------|
| 1    | **Channel XOR**    | Each pixel's R, G, B channel is XORed with its own derived key.             |
| 2    | **Pixel Shuffle**  | All pixels are reordered using an LCG-based Fisher–Yates shuffle (4 passes). |
| 3    | **Affine Transform** | Each channel value is transformed using `(value × A + B) mod 256`.        |

Decryption applies the same three stages in reverse order.

---

## 🧪 RUNNING TESTS 

```bash
python -m unittest tests.test_cipher -v
```

| Test                                  | What It Checks                                          |
|---------------------------------------|---------------------------------------------------------|
| `test_encrypt_decrypt_roundtrip`      | Encrypt → Decrypt produces the original pixels.         |
| `test_encrypted_differs_from_original`| Encrypted image is different from the source image.     |
| `test_wrong_key_fails_roundtrip`      | Decryption with a wrong key does not recover the image. |
| `test_image_size_preserved`           | Image dimensions remain unchanged after encryption.     |
| `test_derive_returns_correct_count`   | KEY_ENGINE generates exactly 16 subkeys.                |
| `test_derive_is_deterministic`        | Same secret always produces the same keys.              |
| `test_different_secrets_give_different_keys` | Different secrets produce different keys.        |

---

## 📝 ENVIRONMENT VARIABLES (.env)

| Variable        | Default  | Description                                    |
|-----------------|----------|------------------------------------------------|
| `OUTPUT_FORMAT` | `PNG`    | The output image format after encryption.      |
| `KDF_ROUNDS`    | `10000`  | Number of SHA-256 rounds for key derivation.   |

---

## 📌 SUPPORTED IMAGE FORMATS 

`PNG`, `JPG`, `JPEG`, `BMP`, `TIFF`

---

## ⚠️ NOTES 

- The `.env` file is optional. If it is missing, default values are used automatically.
- All encrypted images are saved in **PNG** format by default to avoid quality loss.
- Do not forget your encryption key — there is no key recovery option.
