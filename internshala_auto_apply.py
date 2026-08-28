#!/usr/bin/env python3
"""
Autonomous Internshala Application Bot
Discovers matching internships, fills tailored cover letters and questions, and submits applications.
"""

import time
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

from config import CANDIDATE, RESUME_PATH, DASHBOARD_PATH, BROWSER_PROFILE_DIR
from notifier import send_auth_request_email, send_submission_email, log_event

class InternshalaAutoApplier:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.profile_dir = str(BROWSER_PROFILE_DIR)
        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)

    def run(self, max_applications: int = 3):
        log_event("🚀 Starting Internshala Autonomous Worker...")
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
                # 1. Search for live AI, Python & CV internships in Bangalore
                search_url = "https://internshala.com/internships/artificial-intelligence-ai,computer-vision,data-science,python-django-internship-in-bangalore/"
                log_event(f"Navigating to Internshala search: {search_url}")
                page.goto(search_url, wait_until="domcontentloaded")
                time.sleep(4)

                applied_count = 0
                cards = page.locator(".individual_internship")
                count = cards.count()
                log_event(f"Discovered {count} internship cards on Internshala.")

                for i in range(min(count, 10)):
                    if applied_count >= max_applications:
                        break

                    try:
                        card = cards.nth(i)
                        card.scroll_into_view_if_needed()
                        
                        company_el = card.locator(".company_name")
                        title_el = card.locator(".job-internship-name, .profile")
                        company = company_el.inner_text().strip() if company_el.count() > 0 else f"Company-{i+1}"
                        title = title_el.inner_text().strip() if title_el.count() > 0 else "AI/Software Intern"

                        log_event(f"Evaluating Internshala role: {company} - {title}")

                        # Check apply CTA
                        apply_btn = card.locator("a.view_detail_button, button.btn-primary:has-text('Apply')").first
                        if apply_btn.count() > 0:
                            apply_btn.click()
                            time.sleep(3)

                            # Handle application modal if visible
                            modal_apply = page.locator("#apply_now_button, .apply_now_cta, button:has-text('Apply now')").first
                            if modal_apply.count() > 0 and modal_apply.is_visible():
                                modal_apply.click()
                                time.sleep(2)

                            # Fill Cover Letter
                            cover_box = page.locator("#cover_letter, textarea[name='cover_letter'], textarea")
                            if cover_box.count() > 0 and cover_box.first.is_visible():
                                cover_text = (
                                    "I am a 4th-year CS student at DSCE Bengaluru (CPI: 8.15) with practical experience building "
                                    "real-time computer vision pipelines in OpenCV/YOLO and multi-model AST evaluation engines in Python/PyTorch. "
                                    "I write clean, modular code and can contribute immediately to your engineering workflows. "
                                    "Portfolio & Projects: https://ksuchirreddy.github.io"
                                )
                                cover_box.first.fill(cover_text)

                            # Radio checks (Availability)
                            radio_yes = page.locator("input[type='radio'][value='yes'], input[type='radio'][value='Yes']").first
                            if radio_yes.count() > 0 and radio_yes.is_visible():
                                radio_yes.check()

                            # Submit
                            submit_btn = page.locator("#submit, input[type='submit'], button:has-text('Submit')").first
                            if submit_btn.count() > 0 and submit_btn.is_visible():
                                submit_btn.click()
                                time.sleep(2)
                                applied_count += 1
                                log_event(f"✅ Successfully submitted Internshala application for {company} ({title})")
                                send_submission_email("Internshala", company, title, "Submitted via automated script")

                    except Exception as e:
                        log_event(f"Error on Internshala card #{i+1}: {e}")
                        time.sleep(1)

                log_event(f"🎉 Internshala run complete. Total submitted: {applied_count}")

            finally:
                context.close()

if __name__ == "__main__":
    applier = InternshalaAutoApplier(headless=False)
    applier.run(max_applications=3)
