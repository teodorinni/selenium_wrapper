import os

from selenium import webdriver


class WebDriverFactory:

    @staticmethod
    def get_web_driver():
        browser = get_browser().lower()
        if browser == "chrome":
            driver = webdriver.Chrome()
        elif browser == "firefox":
            driver = webdriver.Firefox()
        else:
            raise RuntimeError("Browser not supported. Supported browsers: Chrome, Firefox")
        return driver


def get_browser():
    return os.getenv("BROWSER")
