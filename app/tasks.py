import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from urllib.parse import urljoin

from database import SessionLocal
from crud import create_screenshot


# TODO: Add functionality to close popups on page visit
# TODO: Add func to scroll to bottom of page
# TODO: Add logging to file and notifications on failures for example
class Collector:
    # TODO: redundant naming of app/app from workdir + app dir, consider renaming
    SCREENSHOT_DIR = "/screenshots"

    def __init__(
            self,
            run_id,
            start_url,
            num_links,
    ):
        self.run_id = run_id
        self.start_url = start_url
        self.num_links = num_links
        self.db = SessionLocal()
        self.links_to_follow = []
        self.run_screenshot_dir = None
        self.driver = None

    def get_run_screenshot_dir(self):
        print(f'run_screenshot_dir: {self.run_screenshot_dir}')
        if self.run_screenshot_dir is None:
            print(self.SCREENSHOT_DIR, self.run_id, self.run_screenshot_dir)
            self.run_screenshot_dir = os.path.join(self.SCREENSHOT_DIR, self.run_id)
            os.makedirs(self.run_screenshot_dir, exist_ok=True)
        return self.run_screenshot_dir

    def get_driver(self):
        if self.driver is None:
            # copy pasted solution for chromium error
            options = ChromeOptions()
            options.add_argument("--headless")
            # *** REQUIRED for Docker/Linux container environments ***
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            # --- Optional but recommended ---
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")

            # *** FIX: Unique user data directory per run ***
            user_data_path = f"/tmp/chrome_profile_{self.run_id}"
            options.add_argument(f"--user-data-dir={user_data_path}")
            print(f"[{self.run_id}] Using user data dir: {user_data_path}")

            self.driver = webdriver.Chrome(options=options)

        return self.driver

    # maybe just use driver.get?
    def go_to_url(self, url):
        self.driver.get(url)
        # Wait for page to load for 2 sec - not ideal
        # TODO: implicit wait/selenium method to wait  better
        time.sleep(2)

    def capture_screenshot(self, n_link):
        self.driver.save_screenshot(os.path.join(
            self.run_screenshot_dir,
            f"{n_link}.png")
        )
        print(f"Saved screenshot: {n_link}.png")
        create_screenshot(
            db=self.db,
            run_id=self.run_id,
            filepath=os.path.join(self.run_screenshot_dir, f"{n_link}.png")
        )

    def get_links_to_follow(self):
        elements = self.driver.find_elements(By.TAG_NAME, 'a')
        found_urls = set()
        for elem in elements:
            href = elem.get_attribute('href')
            if href:
                absolute_url = urljoin(self.start_url, href.strip())
                if absolute_url != self.start_url and absolute_url not in found_urls:
                    found_urls.add(absolute_url)
                    if len(self.links_to_follow) < self.num_links:
                        self.links_to_follow.append(absolute_url)
                    else:
                        break
        print(f"Identified {len(self.links_to_follow)} unique links to follow.")

    def crawl_and_capture(self):
        # TODO: Improve rrror handling
        # the try except here is more cosmetic and to ensure db session closing
        try:
            self.get_run_screenshot_dir()
            self.get_driver()
            self.go_to_url(self.start_url)
            self.capture_screenshot("0")
            self.get_links_to_follow()
            for i, link_url in enumerate(self.links_to_follow):
                print(f"{i+1}/{len(self.links_to_follow)}")
                self.go_to_url(link_url)
                self.capture_screenshot(i+1)
            print(f"[{self.run_id}] Task processing completed.")

        except Exception as e:
            print(f"[{self.run_id}] Task failed with error: {e}")
            raise e

        finally:
            if self.driver:
                self.driver.quit()
            if self.db:
                self.db.close()
            print(f"[{self.run_id}] DB & Driver closed.")


# A top level function to instantiate and start the collector class
def run_collector_task(run_id: str, start_url: str, num_links: int):
    collector = Collector(run_id, start_url, num_links)
    collector.crawl_and_capture()
