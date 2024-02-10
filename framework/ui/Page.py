import os

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from framework.ui.webdriver.WebDriverSingleton import WebDriverSingleton


class Page:

    __DEFAULT_TIME_OUT_SECONDS = float(os.getenv("DEFAULT_TIME_OUT_SECONDS"))

    __driver = WebDriverSingleton.get_driver()

    # Actions
    def open_page(self, url: str):
        self.__driver.get(url)
        self.__driver.maximize_window()

    @staticmethod
    def close_browser():
        WebDriverSingleton.get_driver().quit()

    def refresh_page(self):
        self.__driver.refresh()

    def close_page(self):
        self.__driver.close()

    def go_back(self):
        self.__driver.back()

    def go_forward(self):
        self.__driver.forward()
        return self

    def get_cookies(self) -> list[dict]:
        return self.__driver.get_cookies()

    def clear_cookies(self):
        self.__driver.delete_all_cookies()

    def make_screenshot(self, file_path: str):
        return self.__driver.get_screenshot_as_file(file_path)

    def make_full_page_screenshot(self, file_path: str):
        return self.__driver.get_full_page_screenshot_as_file(file_path)

    def get_url(self):
        return self.__driver.current_url

    def switch_to_last_window(self):
        current_window = self.__driver.current_window_handle
        all_windows: list = self.__driver.window_handles
        if current_window == all_windows[0]:
            self.__driver.switch_to.window(all_windows[len(all_windows) - 1])

    def switch_to_first_window(self):
        all_windows: list = self.__driver.window_handles
        if len(all_windows) > 1:
            self.__driver.switch_to.window(all_windows[0])

    def execute_javascript(self, script, *args):
        return self.__driver.execute_script(script, *args)

    def scroll_page_to_top(self):
        return self.execute_javascript("window.scrollTo(0, 0);")

    def scroll_page_to_bottom(self):
        return self.execute_javascript("window.scrollTo(0, document.body.scrollHeight)")

    def open_page_in_new_tab(self, url: str):
        return self.execute_javascript("window.open('{}');".format(url))

    def close_last_tab(self):
        all_windows: list = self.__driver.window_handles
        if len(all_windows) > 1:
            self.__driver.switch_to.window(all_windows[len(all_windows) - 1])
            self.__driver.close()
            self.__driver.switch_to.window(all_windows[len(all_windows) - 2])

    # Waits
    def wait_for_number_of_windows_to_be(self, number_of_windows: int):
        return self.__get_web_driver_wait().until(
            ec.number_of_windows_to_be(number_of_windows))

    def wait_until_title_contains_text(self, text: str):
        return self.__get_web_driver_wait().until(
            ec.title_contains(text))

    def wait_for_title_to_be(self, title: str):
        return self.__get_web_driver_wait().until(
            ec.title_is(title))

    def wait_until_url_changes(self, expected_url: str):
        return self.__get_web_driver_wait().until(
            ec.url_changes(expected_url))

    def wait_until_url_contains(self, text: str):
        return self.__get_web_driver_wait().until(
            ec.url_contains(text))

    def wait_until_url_matches_pattern(self, pattern: str):
        return self.__get_web_driver_wait().until(
            ec.url_matches(pattern))

    def wait_for_url_to_be(self, expected_url: str):
        return self.__get_web_driver_wait().until(
            ec.url_to_be(expected_url))

    # WebDriver related
    def __get_web_driver_wait(self) -> WebDriverWait:
        return WebDriverWait(self.__driver, Page.__DEFAULT_TIME_OUT_SECONDS)
