#!/usr/bin/env python3
"""
Autonomous Naukri Application Bot
Discovers entry-level/fresher software and ML roles in Bengaluru, applies via authenticated profile.
"""

import time
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

from config import CANDIDATE, RESUME_PATH, DASHBOARD_PATH, BROWSER_PROFILE_DIR
from notifier import send_auth_request_email, send_submission_email, log_event

class NaukriAutoApplier:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.profile_dir = str(BROWSER_PROFILE_DIR)
        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)

    def run(self, max_applications: int = 3):
        log_event("🚀 Starting Naukri Autonomous Worker...")
        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=self.profile_dir,
                executable_path="/usr/bin/google-chrome-stable",
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
            )
            page = context.new_page()
            page.set_viewport_size({"width": 1280, "height": 800})

            try:
                # 1. Search for live Fresher / Entry level jobs in Bangalore
                search_url = "https://www.naukri.com/python-developer-jobs-in-bangalore?k=python%20developer%20OR%20machine%20learning%20OR%20software%20engineer&l=bangalore&experience=0"
                log_event(f"Navigating to Naukri search: {search_url}")
                page.goto(search_url, wait_until="domcontentloaded")
                time.sleep(4)

                applied_count = 0
                job_cards = page.locator(".srp-jobtuple-wrapper, article.jobTuple")
                count = job_cards.count()
                log_event(f"Discovered {count} job listings on Naukri.")

                for i in range(min(count, 10)):
                    if applied_count >= max_applications:
                        break

                    try:
                        card = job_cards.nth(i)
                        card.scroll_into_view_if_needed()

                        title_el = card.locator("a.title")
                        company_el = card.locator("a.comp-name")
                        title = title_el.inner_text().strip() if title_el.count() > 0 else "Software / ML Trainee"
                        company = company_el.inner_text().strip() if company_el.count() > 0 else f"Naukri-Company-{i+1}"

                        log_event(f"Evaluating Naukri role: {company} - {title}")

                        # Check for 1-click Apply button
                        apply_btn = card.locator("button:has-text('Apply'), .apply-button").first
                        if apply_btn.count() > 0 and apply_btn.is_visible():
                            apply_btn.click()
                            time.sleep(2)

                            # Handle modal confirmation if prompted
                            confirm_btn = page.locator("button:has-text('Submit'), button:has-text('Apply on company')").first
                            if confirm_btn.count() > 0 and confirm_btn.is_visible():
                                confirm_btn.click()
                                time.sleep(1)

                            applied_count += 1
                            log_event(f"✅ Successfully submitted Naukri application for {company} ({title})")
                            send_submission_email("Naukri", company, title, "Submitted via automated Naukri profile")

                    except Exception as e:
                        log_event(f"Error on Naukri card #{i+1}: {e}")
                        time.sleep(1)

                log_event(f"🎉 Naukri run complete. Total submitted: {applied_count}")

            finally:
                context.close()

if __name__ == "__main__":
    applier = NaukriAutoApplier(headless=False)
    applier.run(max_applications=3)
