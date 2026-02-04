# ─────────────────────────────────────────────────────────────
# core/utils.py
# File-system helpers: search, browse, scan — original IMAGE_UTILS.
# ─────────────────────────────────────────────────────────────

import os
from pathlib import Path
from typing import List, Optional

from config.settings import CONFIG, GREEN, YELLOW, WHITE, RESET


class IMAGE_UTILS:
    # ── Directory-tree search by filename ────────────────────
    @staticmethod
    def SEARCH_IMAGES(NAME: str, START_PATH: str = ".") -> List[Path]:
        RESULTS = []
        START = Path(START_PATH).expanduser().resolve()

        print(f"{YELLOW}SEARCHING FOR '{NAME}'...{RESET}")

        try:
            for ROOT, DIRS, FILES in os.walk(START):
                DIRS[:] = [D for D in DIRS if not D.startswith('.')]

                for FILE in FILES:
                    if NAME.lower() in FILE.lower():
                        FILE_PATH = Path(ROOT) / FILE
                        if FILE_PATH.suffix.upper() in CONFIG.FORMATS:
                            RESULTS.append(FILE_PATH)

                if len(RESULTS) > 50:
                    break

        except PermissionError:
            pass

        return RESULTS

    # ── Interactive folder browser ───────────────────────────
    @staticmethod
    def BROWSE_FOLDER(START_PATH: str = ".") -> Optional[Path]:
        CURRENT = Path(START_PATH).expanduser().resolve()

        while True:
            print(f"\n{GREEN}CURRENT FOLDER: {CURRENT}{RESET}")
            print(f"{WHITE}{'=' * 60}{RESET}")

            ITEMS = []

            if CURRENT.parent != CURRENT:
                ITEMS.append(("📁 ..", CURRENT.parent, True))

            try:
                for ITEM in sorted(CURRENT.iterdir()):
                    if ITEM.is_dir() and not ITEM.name.startswith('.'):
                        ITEMS.append((f"📁 {ITEM.name}", ITEM, True))
            except PermissionError:
                print(f"{YELLOW}PERMISSION DENIED{RESET}")
                return None

            for ITEM in sorted(CURRENT.iterdir()):
                if ITEM.is_file() and ITEM.suffix.upper() in CONFIG.FORMATS:
                    SIZE = ITEM.stat().st_size / 1024
                    ITEMS.append((f"🖼️  {ITEM.name} ({SIZE:.1f} KB)", ITEM, False))

            if not ITEMS:
                print(f"{YELLOW}EMPTY FOLDER{RESET}")
                return None

            for IDX, (LABEL, _, _) in enumerate(ITEMS, 1):
                print(f"{WHITE}[ {IDX} ] {LABEL}{RESET}")

            print(f"{WHITE}[ 0 ] CANCEL{RESET}")
            print()

            CHOICE = input(">> ").strip()

            if CHOICE == "0":
                return None

            try:
                IDX = int(CHOICE) - 1
                if 0 <= IDX < len(ITEMS):
                    _, PATH, IS_DIR = ITEMS[IDX]
                    if IS_DIR:
                        CURRENT = PATH
                    else:
                        return PATH
            except ValueError:
                print(f"{YELLOW}INVALID INPUT{RESET}")

    # ── Flat directory scan ──────────────────────────────────
    @staticmethod
    def SCAN_DIRECTORY(DIR_PATH: str = ".") -> List[Path]:
        DIR = Path(DIR_PATH).expanduser().resolve()

        if not DIR.is_dir():
            print(f"{YELLOW}NOT A DIRECTORY{RESET}")
            return []

        IMAGES = []
        print(f"{GREEN}SCANNING: {DIR}{RESET}")

        try:
            for ITEM in sorted(DIR.iterdir()):
                if ITEM.is_file() and ITEM.suffix.upper() in CONFIG.FORMATS:
                    IMAGES.append(ITEM)
        except PermissionError:
            print(f"{YELLOW}PERMISSION DENIED{RESET}")
            return []

        return IMAGES
