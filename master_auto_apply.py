#!/usr/bin/env python3
"""
Master AI Autonomous Application Runner
Executes automated applications across LinkedIn, Internshala, and Naukri.
"""

import sys
import argparse
from linkedin_easy_apply import LinkedInEasyApplier
from internshala_auto_apply import InternshalaAutoApplier
from naukri_auto_apply import NaukriAutoApplier
from notifier import log_event

def run_master(platform="all", headless=False, count_per_platform=3):
    log_event("🚀 ========================================================")
    log_event(f"🚀 LAUNCHING MASTER AUTO-APPLY ENGINE (Platform: {platform})")
    log_event("🚀 ========================================================")

    if platform in ["linkedin", "all"]:
        log_event("\n--- [1/3] EXECUTING LINKEDIN EASY APPLY ---")
        try:
            li = LinkedInEasyApplier(headless=headless)
            li.run(max_applications=count_per_platform)
        except Exception as e:
            log_event(f"LinkedIn run error: {e}")

    if platform in ["internshala", "all"]:
        log_event("\n--- [2/3] EXECUTING INTERNSHALA APPLY ---")
        try:
            is_app = InternshalaAutoApplier(headless=headless)
            is_app.run(max_applications=count_per_platform)
        except Exception as e:
            log_event(f"Internshala run error: {e}")

    if platform in ["naukri", "all"]:
        log_event("\n--- [3/3] EXECUTING NAUKRI APPLY ---")
        try:
            nk = NaukriAutoApplier(headless=headless)
            nk.run(max_applications=count_per_platform)
        except Exception as e:
            log_event(f"Naukri run error: {e}")

    log_event("\n🎉 Master application suite execution finished.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master Autonomous Job & Internship Application Suite")
    parser.add_argument("--platform", choices=["linkedin", "internshala", "naukri", "all"], default="all")
    parser.add_argument("--headless", action="store_true", help="Run browser in background")
    parser.add_argument("--count", type=int, default=3, help="Applications per platform")
    args = parser.parse_args()

    run_master(platform=args.platform, headless=args.headless, count_per_platform=args.count)
