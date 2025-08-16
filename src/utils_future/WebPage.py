import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from utils import Log

log = Log("WebPage")


class WebPage:
    def __init__(self, url):
        self.url = url
        self.driver = None

    def open(self):
        assert self.driver is None
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(
            options=options, service=Service(log_path="chromedriver.log")
        )
        self.driver.set_window_size(3200, 3200)
        self.driver.get(self.url)
        self.sleep(3)
        return self.driver

    def quit(self):
        if self.driver:
            self.driver.quit()

    def sleep(self, t):
        log.debug(f"😴 {t}s")
        time.sleep(t)
