import os
import time
from urllib.parse import urljoin, urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By

from .database import SessionLocal
from crud import create_screenshot


class Collector:
    SCREENSHOT_DIR = "/app/screenshots"

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
        if self.run_screenshot_dir is None:
            self.run_screenshot_dir = os.path.join(self.SCREENSHOT_DIR, self.run_id)
            os.makedirs(self.run_screenshot_dir, exist_ok=True)
        return self.run_screenshot_dir
    
    def get_driver(self):
        if self.driver is None:
            options = ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
        return self.driver
    
    # maybe just use driver.get
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

        finally:
            if self.driver:
                self.driver.quit()
            if self.db:
                self.db.close()
            print(f"[{self.run_id}] Database session closed.")
