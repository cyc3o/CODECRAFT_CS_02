#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ─────────────────────────────────────────────────────────────
# main.py   ◄── ENTRY POINT  (python main.py)
# ─────────────────────────────────────────────────────────────

import sys

from config.settings import RESET, WHITE, DIM
from services.image_service import (
    handle_encrypt_decrypt,
    handle_search,
    handle_browse,
    handle_scan,
)

# ── ASCII Banner (original, untouched) ───────────────────────
ASCII_BANNER = f"""{WHITE}
　　┏━━┓
      ┃　　┃
   ▕　┏┓　▏　
━╋━┻┻━╋━
   ╱▔╲╱▔╲
▕　▊▕　▊▕
▕╲▁╱╲▁╱▏
   ╲　╲╱　╱            @cyc3o
      ╲     ╱
╭╭╭▏▕╮╮╮
╲╲╲▏▕╱╱╱
   ╲╱　　╲╱
   ▕         ▕
      ╲▁▁╱
         ┃┃
{RESET}
"""

CREDIT = f"{DIM}CREATED BY VISHAL THAKUR{RESET}"


# ── Menu ──────────────────────────────────────────────────────
def MAIN():
    print(ASCII_BANNER)
    print(f"{WHITE}[ 1 ] ENCRYPT IMAGE{RESET}")
    print(f"{WHITE}[ 2 ] DECRYPT IMAGE{RESET}")
    print(f"{WHITE}[ 3 ] SEARCH IMAGE BY NAME{RESET}")
    print(f"{WHITE}[ 4 ] BROWSE & SELECT IMAGE{RESET}")
    print(f"{WHITE}[ 5 ] SCAN ALL IMAGES IN FOLDER{RESET}")
    print(f"{WHITE}[ 6 ] QUIT{RESET}")
    print()
    print(CREDIT)
    print()

    CHOICE = input(">> ").strip()

    if CHOICE == "6":
        sys.exit(0)
    elif CHOICE in ("1", "2"):
        handle_encrypt_decrypt(CHOICE)
    elif CHOICE == "3":
        handle_search()
    elif CHOICE == "4":
        handle_browse()
    elif CHOICE == "5":
        handle_scan()
    else:
        print("INVALID OPTION")


if __name__ == "__main__":
    MAIN()
