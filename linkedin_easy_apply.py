#!/usr/bin/env python3
"""
Autonomous LinkedIn Easy Apply Bot
Finds active Easy Apply roles in Bengaluru, fills the multi-step modal,
uploads resume.pdf, answers standard questions, and clicks 'Submit application'.
"""

import time
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

from config import CANDIDATE, RESUME_PATH, DASHBOARD_PATH, BROWSER_PROFILE_DIR
from notifier import send_auth_request_email, send_submission_email, log_event

class LinkedInEasyApplier:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.profile_dir = str(BROWSER_PROFILE_DIR)
        Path(self.profile_dir).mkdir(parents=True, exist_ok=True)
        self.resume_path = str(RESUME_PATH)

    def run(self, max_applications: int = 3):
        log_event("🚀 Starting LinkedIn Easy Apply Autonomous Worker...")
        with sync_playwright() as p:
            # Launch persistent browser with imported Google Chrome profile
            context = p.chromium.launch_persistent_context(
                user_data_dir=self.profile_dir,
                executable_path="/usr/bin/google-chrome-stable",
                headless=self.headless,
                args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
            )
            page = context.new_page()
            page.set_viewport_size({"width": 1280, "height": 800})

            try:
                # 1. Verify LinkedIn Login
                page.goto("https://www.linkedin.com/jobs/", wait_until="domcontentloaded")
                time.sleep(3)

                if "login" in page.url or "checkpoint" in page.url or page.locator("input#username").count() > 0:
                    log_event("⚠️ User login required for LinkedIn.")
                    send_auth_request_email("LinkedIn", "LinkedIn Portal", "Easy Apply Session", "Please log into LinkedIn in the browser window", page.url)
                    print("\n" + "="*60)
                    print("🔔 ACTION REQUIRED: Please log into LinkedIn in the browser window.")
                    print("Once logged in, press ENTER in this terminal to start auto-applying.")
                    print("="*60 + "\n")
                    try:
                        input("Press [Enter] after logging in: ")
                    except Exception:
                        pass

                # 2. Search for live Easy Apply Jobs in Bengaluru
                search_url = "https://www.linkedin.com/jobs/search/?f_AL=true&keywords=Software%20Engineer%20Intern%20OR%20Python%20Developer%20OR%20AI%20Intern&location=Bengaluru"
                log_event(f"Navigating to Easy Apply search: {search_url}")
                page.goto(search_url, wait_until="domcontentloaded")
                time.sleep(5)

                try:
                    page.wait_for_selector("li[data-occludable-job-id], .job-card-container, .jobs-search-results__list-item, .scaffold-layout__list-item", timeout=12000)
                except Exception:
                    pass

                job_cards = page.locator("li[data-occludable-job-id], .job-card-container, .jobs-search-results__list-item, .scaffold-layout__list-item")
                count = job_cards.count()
                log_event(f"Discovered {count} job cards in search results.")

                applied_count = 0
                for i in range(min(count, 15)):
                    if applied_count >= max_applications:
                        break

                    try:
                        card = job_cards.nth(i)
                        card.scroll_into_view_if_needed()
                        card.click()
                        time.sleep(2)

                        # Get Title & Company
                        title_el = page.locator(".job-details-jobs-unified-top-card__job-title, .jobs-unified-top-card__job-title")
                        company_el = page.locator(".job-details-jobs-unified-top-card__company-name, .jobs-unified-top-card__company-name")
                        title = title_el.inner_text().strip() if title_el.count() > 0 else "Software / AI Intern"
                        company = company_el.inner_text().strip() if company_el.count() > 0 else f"Company-{i+1}"

                        log_event(f"Evaluating: {company} - {title}")

                        # Find Easy Apply button
                        easy_apply_btn = page.locator("button.jobs-apply-button, button:has-text('Easy Apply')").first
                        if easy_apply_btn.count() == 0 or not easy_apply_btn.is_visible():
                            log_event(f"⏩ Easy Apply button not found or already applied for {company}. Skipping.")
                            continue

                        easy_apply_btn.click()
                        time.sleep(2)

                        # Process multi-step modal
                        success = self.fill_easy_apply_modal(page, company, title)
                        if success:
                            applied_count += 1
                            log_event(f"✅ Successfully submitted application for {company} ({title})")
                            send_submission_email("LinkedIn", company, title, "Submitted via automated Easy Apply")
                            time.sleep(3)

                    except Exception as e:
                        log_event(f"Encountered error on job #{i+1}: {e}")
                        time.sleep(1)

                log_event(f"🎉 Completed! Total applications submitted: {applied_count}")

            finally:
                context.close()

    def fill_easy_apply_modal(self, page, company: str, title: str) -> bool:
        """Navigates through the Easy Apply modal pages, fills inputs, and clicks submit."""
        max_steps = 8
        for step in range(max_steps):
            time.sleep(1.5)

            # Check if submitted / done screen
            done_btn = page.locator("button:has-text('Done'), button[aria-label='Dismiss']").first
            if page.locator("h3:has-text('Application sent')").count() > 0 or page.locator("span:has-text('Your application was sent')").count() > 0:
                if done_btn.count() > 0:
                    done_btn.click()
                return True

            # 1. Fill Text Inputs / Phone
            phone_inputs = page.locator("input[type='tel'], input[id*='phoneNumber'], input[id*='phone']")
            if phone_inputs.count() > 0 and phone_inputs.first.is_visible():
                val = phone_inputs.first.input_value()
                if not val:
                    phone_inputs.first.fill("7899597757")

            # 2. Upload Resume if required
            upload_inputs = page.locator("input[type='file']")
            if upload_inputs.count() > 0 and Path(self.resume_path).exists():
                try:
                    upload_inputs.first.set_input_files(self.resume_path)
                    log_event("Attached resume.pdf to application modal.")
                except Exception:
                    pass

            # 3. Numeric questions (Years of experience, CPI)
            numeric_inputs = page.locator("input[type='number'], input[id*='experience'], input[id*='numeric']")
            for j in range(numeric_inputs.count()):
                inp = numeric_inputs.nth(j)
                if inp.is_visible() and not inp.input_value():
                    inp.fill("1")

            # 4. Check Radio buttons (Yes to work authorization / in Bengaluru, No to sponsorship)
            radios = page.locator("input[type='radio']")
            for k in range(radios.count()):
                r = radios.nth(k)
                if r.is_visible() and not r.is_checked():
                    label = page.locator(f"label[for='{r.get_attribute('id')}']").inner_text().lower() if r.get_attribute("id") else ""
                    if "sponsor" in label:
                        if "no" in label:
                            r.check()
                    else:
                        if "yes" in label:
                            r.check()

            # 5. Look for Next / Review / Submit Button
            submit_btn = page.locator("button:has-text('Submit application'), button[aria-label='Submit application']").first
            if submit_btn.count() > 0 and submit_btn.is_visible():
                log_event(f"Clicking final 'Submit application' button for {company}...")
                submit_btn.click()
                time.sleep(2)
                # Dismiss confirmation if shown
                dismiss = page.locator("button[aria-label='Dismiss'], button:has-text('Done')").first
                if dismiss.count() > 0 and dismiss.is_visible():
                    dismiss.click()
                return True

            review_btn = page.locator("button:has-text('Review'), button[aria-label='Review your application']").first
            if review_btn.count() > 0 and review_btn.is_visible():
                review_btn.click()
                continue

            next_btn = page.locator("button:has-text('Next'), button[aria-label='Continue to next step']").first
            if next_btn.count() > 0 and next_btn.is_visible():
                next_btn.click()
                continue

            # If no buttons matched, break
            break

        return False

if __name__ == "__main__":
    applier = LinkedInEasyApplier(headless=False)
    applier.run(max_applications=3)
