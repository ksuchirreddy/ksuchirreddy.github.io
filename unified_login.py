#!/usr/bin/env python3
"""
1-Time Unified Login Session Initializer
Opens LinkedIn, Internshala, and Naukri in a visible browser window.
Once you log in, all cookies & tokens are saved in .browser_profile for automated applications.
"""

from playwright.sync_api import sync_playwright
from config import BROWSER_PROFILE_DIR

def run_login():
    print("\n" + "="*65)
    print("🚀 LAUNCHING UNIFIED LOGIN WINDOW FOR LINKEDIN, INTERNSHALA & NAUKRI")
    print("="*65)
    print("1. The browser window will open with 3 tabs.")
    print("2. Log into LinkedIn, Internshala, and Naukri.")
    print("3. When you are logged into all three, return here and press ENTER.")
    print("="*65 + "\n")

    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_PROFILE_DIR),
            executable_path="/usr/bin/google-chrome-stable",
            headless=False,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )

        # Tab 1: LinkedIn
        p_li = ctx.new_page()
        p_li.goto("https://www.linkedin.com/login")

        # Tab 2: Internshala
        p_is = ctx.new_page()
        p_is.goto("https://internshala.com/login/user")

        # Tab 3: Naukri
        p_nk = ctx.new_page()
        p_nk.goto("https://www.naukri.com/nlogin/login")

        try:
            input("👉 Press [ENTER] in this terminal AFTER logging into all 3 platforms: ")
        except Exception:
            pass

        ctx.close()
        print("\n✅ Session tokens saved permanently to .browser_profile! You can now run master_auto_apply.py.")

if __name__ == "__main__":
    run_login()
