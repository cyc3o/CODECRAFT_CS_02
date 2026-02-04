# ─────────────────────────────────────────────────────────────
# services/image_service.py
# Business-logic layer.  MAIN() ke har option ka handler yahan hai.
# Cipher / Utils ko directly touch nahi karta user — yeh layer karta hai.
# ─────────────────────────────────────────────────────────────

from pathlib import Path

from config.settings import GREEN, YELLOW, RESET, WHITE
from core.image_loader import IMAGE_CIPHER
from core.utils import IMAGE_UTILS


# ── shared helper: user se encrypt/decrypt choice + run ──────
def _run_cipher(SRC: str, KE=None):
    """OUTPUT path + KEY poochta hai, phir encrypt/decrypt chalata hai."""
    DST = input("OUTPUT IMAGE PATH: ").strip()
    KEY = input("ENTER KEY        : ").strip()
    MODE = input("[ 1 ] ENCRYPT  [ 2 ] DECRYPT >> ").strip()

    ENGINE = IMAGE_CIPHER()
    try:
        if MODE == "1":
            ENGINE.ENCRYPT(SRC, DST, KEY)
            print(f"{GREEN}ENCRYPTION COMPLETED{RESET}")
        elif MODE == "2":
            ENGINE.DECRYPT(SRC, DST, KEY)
            print(f"{GREEN}DECRYPTION COMPLETED{RESET}")
        else:
            print(f"{YELLOW}INVALID MODE{RESET}")
    except Exception as E:
        print(f"ERROR: {E}")


# ── Option 1 / 2  — manual path input ───────────────────────
def handle_encrypt_decrypt(CHOICE: str):
    SRC = input("INPUT IMAGE PATH : ").strip()
    DST = input("OUTPUT IMAGE PATH: ").strip()
    KEY = input("ENTER KEY        : ").strip()

    ENGINE = IMAGE_CIPHER()
    try:
        SRC_PATH = Path(SRC)
        if SRC_PATH.is_dir():
            print("ERROR: INPUT PATH IS A FOLDER")
            print("TIP  : USE FULL IMAGE FILE PATH")
            return

        DST_PATH = Path(DST)
        if DST_PATH.is_dir():
            DST_PATH = DST_PATH / "output.png"
            print(f"INFO : OUTPUT SET TO {DST_PATH}")

        if CHOICE == "1":
            ENGINE.ENCRYPT(str(SRC_PATH), str(DST_PATH), KEY)
            print(f"{GREEN}ENCRYPTION COMPLETED{RESET}")
        elif CHOICE == "2":
            ENGINE.DECRYPT(str(SRC_PATH), str(DST_PATH), KEY)
            print(f"{GREEN}DECRYPTION COMPLETED{RESET}")
        else:
            print("INVALID OPTION")

    except ValueError as E:
        print(f"ERROR: {E}")
        print("TIP  : USE VALID IMAGE FILE (.PNG, .JPG, .JPEG)")
    except Exception as E:
        print("UNEXPECTED ERROR")
        print(E)


# ── Option 3  — search by name ───────────────────────────────
def handle_search():
    NAME  = input("IMAGE NAME TO SEARCH: ").strip()
    START = input("START PATH (PRESS ENTER FOR CURRENT): ").strip() or "."

    RESULTS = IMAGE_UTILS.SEARCH_IMAGES(NAME, START)

    if not RESULTS:
        print(f"{YELLOW}NO IMAGES FOUND{RESET}")
        return

    print(f"\n{GREEN}FOUND {len(RESULTS)} IMAGE(S):{RESET}")
    for IDX, IMG in enumerate(RESULTS, 1):
        print(f"{WHITE}[ {IDX} ] {IMG}{RESET}")
    print(f"{WHITE}[ 0 ] CANCEL{RESET}\n")

    SELECT = input("SELECT IMAGE NUMBER: ").strip()
    try:
        IDX = int(SELECT) - 1
        if 0 <= IDX < len(RESULTS):
            SRC = str(RESULTS[IDX])
            print(f"{GREEN}SELECTED: {SRC}{RESET}")
            _run_cipher(SRC)
        # else: silently cancel (original behavior)
    except ValueError:
        return


# ── Option 4  — interactive folder browser ──────────────────
def handle_browse():
    START = input("START PATH (PRESS ENTER FOR CURRENT): ").strip() or "."

    SELECTED = IMAGE_UTILS.BROWSE_FOLDER(START)

    if not SELECTED:
        print(f"{YELLOW}NO IMAGE SELECTED{RESET}")
        return

    SRC = str(SELECTED)
    print(f"{GREEN}SELECTED: {SRC}{RESET}")
    _run_cipher(SRC)


# ── Option 5  — scan folder listing ─────────────────────────
def handle_scan():
    DIR = input("FOLDER PATH (PRESS ENTER FOR CURRENT): ").strip() or "."

    IMAGES = IMAGE_UTILS.SCAN_DIRECTORY(DIR)

    if not IMAGES:
        print(f"{YELLOW}NO IMAGES FOUND{RESET}")
        return

    print(f"\n{GREEN}FOUND {len(IMAGES)} IMAGE(S):{RESET}")
    print(f"{WHITE}{'=' * 60}{RESET}")
    for IMG in IMAGES:
        SIZE = IMG.stat().st_size / 1024
        print(f"{WHITE}🖼️  {IMG.name:<40} ({SIZE:>8.1f} KB){RESET}")
    print(f"{WHITE}{'=' * 60}{RESET}")
