# 🔐 Image Cipher

RGB pixel-level image encryption — **channel XOR → pixel shuffle → affine transform**.

---

## 📂 Structure

```
image_cipher/
├── main.py                 # 🔥 ENTRY POINT  →  python main.py
├── requirements.txt
├── .env                    # OUTPUT_FORMAT, KDF_ROUNDS
├── .gitignore
│
├── config/
│   └── settings.py         # CONFIG class + terminal colors
│
├── core/
│   ├── cipher.py           # KEY_ENGINE + 3 pipeline stages
│   ├── image_loader.py     # IMAGE_CIPHER  (load / save / encrypt / decrypt)
│   └── utils.py            # IMAGE_UTILS   (search / browse / scan)
│
├── services/
│   └── image_service.py    # Menu handlers (business logic)
│
├── tests/
│   └── test_cipher.py      # Round-trip + KEY_ENGINE unit tests
│
└── assets/
    └── samples/            # Test images rakhein yahan
```

---

## ⚡ Setup

```bash
pip install -r requirements.txt
python main.py
```

---

## 🧠 How It Works

| Step | Stage | What happens |
|------|-------|--------------|
| 1 | **Channel XOR** | Har pixel ka R/G/B apne key se XOR hota hai |
| 2 | **Pixel Shuffle** | LCG-based Fisher–Yates shuffle se pixels ka order badal jaata hai (4 passes) |
| 3 | **Affine Transform** | Har channel value pe `(val * A + B) mod 257` lagta hai |

Decryption mein yahi steps ulta order mein chalte hain.

---

## 🧪 Tests

```bash
python -m pytest tests/
```

| Test | Kya check karta hai |
|------|---------------------|
| `test_encrypt_decrypt_roundtrip` | Encrypt → Decrypt = original pixels |
| `test_encrypted_differs_from_original` | Encrypted image original se alag hai |
| `test_wrong_key_fails_roundtrip` | Galat key se original nahi milta |
| `test_image_size_preserved` | Image dimensions change nahi hote |
| `test_derive_*` | KEY_ENGINE deterministic + unique keys |

---

## 📝 .env Options

| Variable | Default | Meaning |
|----------|---------|---------|
| `OUTPUT_FORMAT` | `PNG` | Output image format |
| `KDF_ROUNDS` | `10000` | Key derivation iterations |
